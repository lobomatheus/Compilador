import re

'''
    A classe token define um tipo token que possui um codigo (inteiro), o 
    token (uma string), o valor do token (a string reconhecida) e um booleano
    que diz se o token é um terminal.
'''

class Token():

    def __init__(self, cod, token, strVal, isTerminal, linha):

        self.cod = cod
        self.token = token
        self.strVal = strVal
        self.isTerminal = isTerminal
        self.linha = linha

    def exhibit(self):
        #print("{- "+str(self.token) + ": " + self.strVal+" na linha " + str(self.linha) + " -}")
        if(self.isTerminal):
            #print(str(self.token))
            return "{- "+str(self.token) + ": " + self.strVal+" na linha " + str(self.linha) + " -}"
        else:
            #print(str(self.cod))
            return "{- <"+str(self.token) + "> na linha " + str(self.linha) + " -}"

    def getSymbol(self):
        return str(self.strVal)
    
    def getLinha(self):
        return self.linha

    def getTokenCode(self):
        return self.cod


#A função matchToken não está dentro da classe token, ela
#apenas instancia um novo token a partir da string dada.
def matchToken(val, linha):
    if(re.match("^program$", val)):
        return Token(1, "TProgram", val, True, linha)
    elif(re.match("^begin$", val)):
        return Token(2, "TBegin", val, True, linha)
    elif(re.match("^end$", val)):
        return Token(3, "TEnd", val, True, linha)
    elif(re.match("^const$", val)):
        return Token(4, "TConst", val, True, linha)
    elif(re.match("^type$", val)):
        return Token(5, "TType", val, True, linha)
    elif(re.match("^var$", val)):
        return Token(6, "TVar", val, True, linha)
    elif(re.match("^array$", val)):
        return Token(7, "TArray", val, True, linha)
    elif(re.match("^of$", val)):
        return Token(8, "TOf", val, True, linha)
    elif(re.match("^record$", val)):
        return Token(9, "TRecord", val, True, linha)
    elif(re.match("^function$", val)):
        return Token(10, "TFunction", val, True, linha)
    elif(re.match("^procedure$", val)):
        return Token(11, "TProcedure", val, True, linha)
    elif(re.match("^integer$", val)):
        return Token(12, "TInteger", val, True, linha)
    elif(re.match("^real$", val)):
        return Token(13, "TReal", val, True, linha)
    elif(re.match("^while$", val)):
        return Token(14, "TWhile", val, True, linha)
    elif(re.match("^if$", val)):
        return Token(15, "TIf", val, True, linha)
    elif(re.match("^then$", val)):
        return Token(16, "TThen", val, True, linha)
    elif(re.match("^write$", val)):
        return Token(17,"TWrite", val, True, linha)
    elif(re.match("^read$", val)):
        return Token(18, "TRead", val, True, linha)
    elif(re.match("^else$", val)):
        return Token(19, "TElse", val, True, linha)
    elif(re.match("^[=><!]$", val)):
        return Token(20, "TRelational",val, True, linha)
    elif(re.match("^[,]$", val)):
        return Token(23, "TVirgula", val, True, linha)
    elif(re.match("^[.]$", val)):
        return Token(28, "TPonto", val, True, linha)
    elif(re.match("^[+-/*]$", val)):
        return Token(21,"TOperator", val, True, linha)
    elif(re.match("^;$", val)):
        return Token(22, "TPontoEVirgula", val, True, linha)
    elif(re.match("^[[]$", val)):
        return Token(24, "TOpColchetes", val, True, linha)
    elif(re.match("^[]]$", val)):
        return Token(25, "TClsColchetes", val, True, linha)
    elif(re.match("^[(]$", val)):
        return Token(26, "TAbreParenteses", val, True, linha)
    elif(re.match("^[)]$", val)):
        return Token(27, "TFechaParenteses", val, True, linha)
    elif(re.match("^[\"][a-zA-Z0-9\s]*[\"]$", val)):
        return Token(29, "TString", val, True, linha)
    elif(re.match("^[:]$", val)):
        return Token(30, "TDoisPontos", val, True, linha)
    elif(re.match("^[a-zA-Z_][:alnum:]*", val)):
        return Token(31, "TAlfaNum", val, True, linha)
    elif(re.match("^[0-9]+$", val)):
        return Token(32, "TNum", val, True, linha)
    elif(re.match("^[0-9]+.[0-9]+$", val)):
        return Token(32, "TNum", val, True, linha)
    elif(re.match("^:=$", val)):
        return Token(33, "TAtribuicao", val, True, linha)
    #else: error
    else:
        if(val != "$"):
            return Token(-1, "TError", val, False, linha)
        else:
            return Token(0, "NT", val, False, linha)