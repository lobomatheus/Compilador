from token import Token, matchToken

'''
Função do Handler é ser o iterador do arquivo. Uma instância dele é guardada no 
programa principal (ou no analisador sintático) e é chamada sempre que o analisador
precisar do próximo token.
'''

class Handler():

    # A main recebe o nome do arquivo do programa e instancia o arquivo 
    def __init__(self, filename):
        self.pos = 0
        self.linha=1
        self.arq = arq = open(filename, "r", encoding="utf8")
        self.currToken = None

    def getLinha(self):
        return self.linha

    def consumeToken(self):
        self.currToken = None

    def getToken(self):
        if(self.currToken != None):
            return self.currToken
        else:
            ret = self.nextToken()
            if(ret == "$"):
                tkn = Token(0, "", "$", False, self.linha)
            else:
                tkn = matchToken(ret, self.linha)
                self.currToken = tkn
            return tkn
        

    # nextToken retorna o próximo token ou $ caso seja um valor inválido (pode ser substituido)
    # por qualquer caracter inválido para a linguagem
    def nextToken(self):
        tkn = ""
        chr = self.arq.read(1)
        self.pos = self.pos+1
        if len(chr) < 1:
            return "$"
        if chr in "abcdefghijklmnopqrstuvwxyzzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            tkn = chr + self.matchLetraNumero()
        elif chr in "1234567890":
            tkn = chr + self.matchNumero(False)
        elif chr == '"':
            tkn = chr + self.matchString()
        elif chr == ':':
            tkn = chr + self.matchAtribuicao()
        #elif chr in "()[]=+-*/;,><!.:":
        #    tkn = chr
        elif (chr == "{"):
            self.matchComentario()
            tkn = self.nextToken()
        elif chr in " \n":
            if(chr == "\n"):
                self.linha = self.linha+1
            tkn = self.nextToken()
        else: tkn = chr
        return tkn

    def matchString(self):
        chr = self.arq.read(1)
        
        if len(chr)<1:
            #error
            raise Exception("Faltando fecha aspas")
            return ""

        self.pos = self.pos+1
        
        if chr == '"' :
            return chr + ""
        else:
            return chr + self.matchString()

    def matchComentario(self):
        chr = self.arq.read(1)

        self.pos = self.pos+1

        if(chr == "}"):
            return
        elif(chr == "\n"):
            self.linha = self.linha + 1
            self.matchComentario()
        else:
            self.matchComentario()

    def matchLetraNumero(self):
        chr = self.arq.read(1)
        if len(chr) < 1:
            return ""
        self.pos = self.pos+1
        if chr in "abcdefghijklmnopqrstuvwxyzzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
            return chr + self.matchLetraNumero()
        
        else:
            self.pos = self.pos-1
            self.arq.seek(self.pos)
            return ""

    def matchNumero(self, isFloat):
        chr = self.arq.read(1)
        if len(chr) < 1:
            return ""
        self.pos = self.pos+1
        if chr in "1234567890":
            return chr + self.matchNumero(isFloat)
        elif(chr == '.' and not isFloat):
            return chr + self.matchNumero(True)
        else:
            self.pos = self.pos-1
            self.arq.seek(self.pos)
            return ""
    
    def matchAtribuicao(self):
        chr = self.arq.read(1)
        self.pos = self.pos+1
        if (chr == '='):
            return chr
        else:
            self.pos = self.pos-1
            self.arq.seek(self.pos)
            return ""