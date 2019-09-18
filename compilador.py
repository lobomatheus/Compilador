import sys
from token import Token, matchToken
from seeker import Handler
from errors import errors
#from sintatico import PROGRAMA

#Essa seria a main do programa. Nela, um handler é instanciado
#e vai solicitando os tokens. Ao invés desse while, teria que ser
#chamado o analisador sintático, passando o handler para que ele
#possa verificar os próximos tokens.

filename = sys.argv[1]
handler = Handler(filename)
tknList = []
err = errors()

#PROGRAMA(handler)
while True:
    t = handler.nextToken()
    linha = handler.getLinha()
    tkn = matchToken(t, linha)
    if(tkn.getTokenCode() == 0):
        break
    elif(tkn.getTokenCode() == -1):
        err.addErr(tkn.getSymbol(), "TError", tkn.getLinha())
    else:
        tknList.append(tkn)
    


for t in tknList:
    t.exhibit()
print(len(tknList))

err.printError()