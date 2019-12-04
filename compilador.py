# -*- coding: utf-8 -*-
import sys
from token import Token, matchToken
from seeker import Handler
from errors import errors
from sintatico import programa, TokenTree
from symb import SymbolTable
from inter import Instrucao, gerarCodigoIntermediario

#Essa seria a main do programa. Nela, um handler é instanciado
#e vai solicitando os tokens. Ao invés desse while, teria que ser
#chamado o analisador sintático, passando o handler para que ele
#possa verificar os próximos tokens.

filename = sys.argv[1]
handler = Handler(filename)
tknList = []
err = errors()
table = SymbolTable()

tree = programa(handler, err, table)
'''while True:
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
'''
tree.printTree(0)
#table.printTable()
flag = err.printError() #Precisa fazer com que ele só gere o código se não tiver erro, mas isso pode ficar pro fim

if(not flag):
    codigo_intermediario = gerarCodigoIntermediario(tree) #aqui vai retornar um array de Instrucao

    line=1
    for inst in codigo_intermediario.conj:
        if(inst.label != None):
            print(str(inst.label) + ' '  + str(line) + ' | ' + str(inst.instrucao))
        else:
            print(str(line) + ' | ' + str(inst.instrucao))
        line = line + 1