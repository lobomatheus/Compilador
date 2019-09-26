class errors:

    def __init__(self):
        self.err = []

    def addErr(self, simb, token, linha, errtype):
        if(errtype == 1):
            message = "Erro léxico no símbolo "
        elif(errtype == 2):
            message = "Erro sintático, faltando "
        elif(errtype == 3):
            message = "Erro semântico no símbolo "
        else:
            message = "Erro no símbolo "
        t = (simb, token, linha, message)
        self.err.append(t)

    def printError(self):
        for e in self.err:
            simb,token,linha,message = e
            print(message + str(simb) + " na linha " + str(linha))
        print("Compilação terminada")