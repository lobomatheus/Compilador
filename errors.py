class errors:

    def __init__(self):
        self.err = []

    def addErr(self, simb, token, linha, errtype):
        if(errtype == 1):
            message = "Erro léxico no símbolo "
        elif(errtype == 2):
            message = "Erro sintático, faltando "
        elif(errtype == 3):
            message = "Erro semântico (identificador não declarado) no símbolo "
        elif(errtype == 4):
            message = "Erro semântico (identificador já declarado) no símbolo "
        elif(errtype == 5):
            message = "Erro semântico (identificador não é array) no símbolo "
        elif(errtype == 6):
            message = "Erro semântico (identificador não é função) no símbolo "
        elif(errtype == 7):
            message = "Erro semântico (identificador não é registro) no símbolo "
        elif(errtype == 8):
            message = "Erro semântico (identificador não é campo do registro) no símbolo "
        elif(errtype == 9):
            message = "Erro semântico (quantidade de parâmetros diferente) no símbolo "
        elif(errtype == 10):
            message = "Erro semântico (tipos não correspondem) no símbolo "
        else:
            message = "Erro no símbolo "
        t = (simb, token, linha, message)
        self.err.append(t)

    def printError(self):
        for e in self.err:
            simb,token,linha,message = e
            print(message + str(simb) + " na linha " + str(linha))
        print("Compilação terminada")