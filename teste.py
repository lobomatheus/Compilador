import sys
from token import Token, matchToken
from seeker import Handler
from sintatico import PROGRAMA

#Essa seria a main do programa. Nela, um handler é instanciado
#e vai solicitando os tokens. Ao invés desse while, teria que ser
#chamado o analisador sintático, passando o handler para que ele
#possa verificar os próximos tokens.

filename = sys.argv[1]
handler = Handler(filename)
tknList = []

#PROGRAMA(handler)
while True:
    tkn = matchToken(handler.nextToken())
    if(tkn.getTokenCode() == -1):
        break
    tknList.append(tkn)
    
for t in tknList:
    t.exhibit()
print(len(tknList))