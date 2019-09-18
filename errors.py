class errors:

    def __init__(self):
        self.err = []

    def addErr(self, simb, token, linha):
        t = (simb, token, linha)
        self.err.append(t)

    def printError(self):
        for e in self.err:
            simb,token,linha = e
            print("Erro léxico no simbolo " + str(simb) + " na linha " + str(linha))
        print("Compilação terminada")