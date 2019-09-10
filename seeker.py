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
        self.arq = arq = open(filename, "r")

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
        elif chr in "()[]=+-*/;,><!.:":
            tkn = chr
        elif chr in " \n":
            tkn = self.nextToken()
        else: raise Exception("Caracter " + chr + " não reconhecido na gramática!")
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
            return chr + self.matchLetraNumero(True)
        else:
            self.pos = self.pos-1
            self.arq.seek(self.pos)
            return ""