from token import *
from seeker import Handler
from follow import *

#Constantes para os token codes
TPROGRAM = 1
TBEGIN = 2
TEND = 3
TCONST=4
TTYPE = 5
TVAR=6
TARRAY=7
TOF = 8
TRECORD = 9
TFUNCTION = 10
TPROCEDURE = 11
TINTEGER = 12
TREAL = 13
TWHILE = 14
TIF = 15
TTHEN = 16
TWRITE = 17
TREAD = 18
TELSE = 19
TRELATIONAL = 20
TVIRGULA = 23
TOPERATOR = 21
TPONTOEVIRGULA = 22
TABRECOLCHETES = 24
TFECHACOLCHETES = 25
TABREPARENTESES = 26
TFECHAPARENTESES = 27
TPONTO = 28
TSTRING = 29
TDOISPONTOS = 30
TID = 31
TNUM = 32
TATRIBUICAO = 33

class TokenTree:

    def __init__(self, node):
        self.node = node
        self.children = []

    def addChild(self, child):
        if((child.node.isTerminal) or (child.hasChildren())):
            self.children.append(child)
    
    def hasChildren(self):
        return (len(self.children) > 0)

    def getRoot(self):
        return self.node

    def printTree(self, space):
        s = ""
        for i in range(space):
            s = s + "-"
        print(s + self.node.exhibit())
        #print(self.children) 
        if(len(self.children) > 0):
            for child in self.children:
                child.printTree(space+2)

# usa essa função aqui pra pegar o próximo token
def getToken(handler, err):
    tkn = handler.getToken()
    if(tkn.getTokenCode() == -1):
        err.addErr(tkn.getSymbol(), "TError", tkn.getLinha(), 1)
        return getToken(handler, err)
    #tkn.exhibit()
    return tkn

#ignora todos os tokens tkn que não pertencerem ao conjunto follow de token 
def panicMode(handler, err, token, tkn):
    #print("modo panico no " + str(token.token) + " na linha " + str(token.getLinha()))
    while (tkn.getTokenCode() not in getFollowsArray(token)):
        handler.consumeToken()
        tkn = getToken(handler, err)
        if(tkn.getTokenCode() == 0):
            #print("FIM DO ARQUIVO")
            break
    return tkn 



#quando encontrar um terminal que você estava procurando, chamar handler.consumeToken()
def programa(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(72, "TPROGRAMA", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPROGRAM):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TID):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
                tree.addChild(Corpo(handler, err, table))
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
                tk = panicMode(handler, err, tree.getRoot(), tk)
        else:
            err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    else:
        err.addErr("program", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def Corpo(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(34, "TCORPO", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TCONST):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(constantes(handler, err, table))
    tree.addChild(Corpo2(handler, err, table))
    return tree

def Corpo2(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(35, "TCORPO2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TTYPE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(tipos(handler, err, table))
    tree.addChild(Corpo3(handler, err, table))
    return tree

def Corpo3(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(36, "TCORPO3", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVAR):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(variaveis(handler, err, table))
    tree.addChild(Corpo4(handler, err, table))
    return tree

def Corpo4(handler, err, table):
    tree = TokenTree(Token(37, "TCORPO4", "", False, getToken(handler, err).getLinha()))
    tree.addChild(def_rotinas(handler, err, table))
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TBEGIN):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(comandos(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TEND):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tk = getToken(handler, err)
            print(tk.exhibit())
            if(tk.getSymbol() != "$"):
                err.addErr("fim de arquivo", tk.getSymbol(), tk.getLinha(), 2)
            print("End")
        else:
            err.addErr("end", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    else:
        err.addErr("begin", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def def_rotinas(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(38, "TDEFROTINAS", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TFUNCTION):
        tree.addChild(TokenTree(tk))
        table.newSymbol('function')
        handler.consumeToken()
        tree.addChild(nome_rotina(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TDOISPONTOS):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(tipo_dado(handler, err, table))
            tree.addChild(bloco_rotina(handler, err, table))
            table.rmEscopo()
            tree.addChild(def_rotinas(handler, err, table))
        else:
            err.addErr(":", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    elif(tk.getTokenCode() == TPROCEDURE):
        tree.addChild(TokenTree(tk))
        table.newSymbol('procedure')
        handler.consumeToken()
        tree.addChild(nome_rotina(handler, err, table))
        tree.addChild(bloco_rotina(handler, err, table))
        table.rmEscopo()
        table.saveSymbol()
        tree.addChild(def_rotinas(handler, err, table))
    return tree

def nome_rotina(handler, err, table):
    tk= getToken(handler, err)
    tree = TokenTree(Token(39, "TNOMEROTINA", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        #if(table.mesmoNome(tk.getSymbol())):
        #    err.addErr(tk.getSymbol(), tk, tk.getLinha(), 4)
        table.addName(tk.getSymbol())
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TABREPARENTESES):
            table.startParam()
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(variaveis(handler, err, table))
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TFECHAPARENTESES):
                table.stopParam()
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
            else:
                err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
                tk = panicMode(handler, err, tree.getRoot(), tk)
        else:
            err.addErr("(", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def bloco_rotina(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(40, "TBLOCOROTINA", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVAR):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(variaveis(handler, err, table))
        tk = getToken(handler, err)
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(bloco_rotina2(handler, err, table))
    else:
        tree.addChild(bloco(handler, err, table))
    return tree

def bloco_rotina2(handler, err, table):
    tk=getToken(handler, err)
    tree = TokenTree(Token(41, "TBLOCOROTINA2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(lista_id3(handler, err, table))
    elif(tk.getTokenCode() == TDOISPONTOS):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(lista_id4(handler, err, table))
    else:
        tree.addChild(nome2(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode()==TATRIBUICAO):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(exp_mat(handler, err, table))
            tk=getToken(handler, err)
            if(tk.getTokenCode()== TPONTOEVIRGULA):
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
                tk = panicMode(handler, err, tree.getRoot(), tk)
        else:
            err.addErr(":=", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def constantes(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(44, "TCONSTANTES", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        table.newSymbol('var')
        table.addName(tk.getSymbol())
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol() == "="):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(const_valor(handler, err, table, True))
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                table.saveSymbol()
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
                tree.addChild(constantes2(handler, err, table))
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
                tk = panicMode(handler, err, tree.getRoot(), tk)
        else:
            err.addErr("=", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def constantes2(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(45, "TCONSTANTES2", "", False, tk.getLinha()))
    if(tk.getTokenCode()==TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(constantes3(handler, err, table))
    return tree

def constantes3(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(46, "TCONSTANTES3", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol()=="="):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(const_valor(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(constantes2(handler, err, table))
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    else:
        err.addErr("=", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree
    
def tipos(handler, err, table):
    tk=getToken(handler, err)
    tree = TokenTree(Token(47, "TTIPOS", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        table.newSymbol('tipo')
        tree.addChild(TokenTree(tk))
        table.addName(tk.getSymbol())
        handler.consumeToken()
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol()=="="):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(tipo_dado(handler, err, table))
            tree.addChild(tipos2(handler, err, table))
        else:
            err.addErr("=", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def tipos2(handler, err, table):
    tk=getToken(handler, err)
    tree = TokenTree(Token(48, "TTIPOS2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPONTOEVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(tipos(handler, err, table))
    return tree

def tipo_dado(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(49, "TTIPODADO", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TINTEGER):
        table.addTipo('int')
        table.saveSymbol()
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
    elif(tk.getTokenCode() == TREAL):
        table.addTipo('real')
        table.saveSymbol()
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
    elif(tk.getTokenCode() == TARRAY):
        tree.addChild(TokenTree(tk))
        table.addTipo(table.arrayNum())
        table.saveSymbol()
        table.newSymbol('array')
        table.addName(table.arrayNum())
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TABRECOLCHETES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TNUM):
                tree.addChild(TokenTree(tk))
                table.addElemNum(tk.getSymbol())
                handler.consumeToken()
                tk = getToken(handler, err)
                if(tk.getTokenCode() == TFECHACOLCHETES):
                    tree.addChild(TokenTree(tk))
                    handler.consumeToken()
                    tk = getToken(handler, err)
                    if(tk.getTokenCode() == TOF):
                        tree.addChild(TokenTree(tk))
                        handler.consumeToken()
                        tree.addChild(tipo_dado(handler, err, table))                        
                    else:
                        err.addErr("of", tk.getSymbol(), tk.getLinha(), 2)
                        tk = panicMode(handler, err, tree.getRoot(), tk)
                else:
                    err.addErr("]", tk.getSymbol(), tk.getLinha(), 2)
                    tk = panicMode(handler, err, tree.getRoot(), tk)
            else:
                err.addErr("numero", tk.getSymbol(), tk.getLinha(), 2)
                tk = panicMode(handler, err, tree.getRoot(), tk)
        else:
            err.addErr("[", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    elif(tk.getTokenCode() == TRECORD):
        tree.addChild(TokenTree(tk))
        table.addTipo('record')
        scope = table.getName()
        table.saveSymbol()
        handler.consumeToken()
        table.addEscopo(scope)
        tree.addChild(variaveis(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TEND):
            table.rmEscopo()
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr("end", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    elif(tk.getTokenCode() == TID):
        table.addTipo(tk.getSymbol())
        table.saveSymbol()
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
    else:
        err.addErr("integer, real, array, record, id", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def variaveis(handler, err, table):
    tree = TokenTree(Token(50, "TVARIAVEIS", "", False, getToken(handler, err).getLinha()))
    table.newSymbol('var')
    tree.addChild(lista_id(handler, err, table))
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TDOISPONTOS):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(tipo_dado(handler, err, table))
        tree.addChild(variaveis2(handler, err, table))
    else:
        err.addErr(":", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def variaveis2(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(51, "TVARIAVEIS2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPONTOEVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(variaveis(handler, err, table))
    return tree

def lista_id(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(52, "TLISTAID", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        table.addName(tk.getSymbol())
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(lista_id2(handler, err, table))
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def lista_id2(handler,err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(53, "TLISTAID2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(lista_id(handler, err, table))
    return tree

def lista_id3(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(42, "TLISTAID3", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(variaveis(handler, err, table))
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def lista_id4(handler, err, table):
    tree = TokenTree(Token(43, "TLISTAID4", "", False, getToken(handler, err).getLinha()))
    tree.addChild(tipo_dado(handler, err, table))
    tree.addChild(variaveis2(handler, err, table))
    return tree
                    
def comandos(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(54, "TCOMANDOS", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TWHILE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err, table))
        tree.addChild(bloco(handler, err, table))
        tree.addChild(comandos2(handler, err, table))
    elif(tk.getTokenCode() == TIF):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TTHEN):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(bloco(handler, err, table))
            tree.addChild(felse(handler, err, table))
            tree.addChild(comandos2(handler, err, table))
        else:
            err.addErr("then", tk.getSymbol, tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    elif(tk.getTokenCode() == TWRITE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(const_valor(handler, err, table))
        tree.addChild(comandos2(handler, err, table))
    elif(tk.getTokenCode() == TREAD):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome(handler, err, table))
        tree.addChild(comandos2(handler, err, table))
    elif(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome2(handler, err, table))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TATRIBUICAO):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(exp_mat(handler, err, table))
            tree.addChild(comandos2(handler, err, table))
        else:
            err.addErr(":=", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def bloco(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(57, "TBLOCO", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TBEGIN):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(comandos(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode()==TEND):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr("end", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    else:
        tree.addChild(comandos3(handler, err, table))
    return tree

def comandos3(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(56, "TCOMANDOS3", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TWHILE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err, table))
        tree.addChild(bloco(handler, err, table))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    elif(tk.getTokenCode() == TIF):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TTHEN):
            tree.addChild(TokenTree(tk))
            tk.consumeToken()
            tree.addChild(bloco(handler, err, table))
            tree.addChild(felse(handler, err, table))
            tk=getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
                tk = panicMode(handler, err, tree.getRoot(), tk)
        else:
            err.addErr("then", tk.getSymbol, tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    elif(tk.getTokenCode() == TWRITE):
        tree.addChild(TokenTree(tk))
        tk.consumeToken()
        tree.addChild(const_valor(handler, err, table))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    elif(tk.getTokenCode() == TREAD):
        tree.addChild(TokenTree(tk))
        tk.consumeToken()
        tree.addChild(nome(handler, err, table))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    elif(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome2(handler, err, table))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TATRIBUICAO):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(exp_mat(handler, err, table))
            tk=getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
                tk = panicMode(handler, err, tree.getRoot(), tk)
        else:
            err.addErr(":=", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def felse(handler, err, table):
    tk=getToken(handler, err)
    tree = TokenTree(Token(58, "TELSE", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TELSE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(bloco(handler, err, table))
    return tree

def const_valor(handler, err,table, adding=False):
    tk = getToken(handler, err)
    tree = TokenTree(Token(59, "TCONSTVALOR", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TSTRING):
        tree.addChild(TokenTree(tk))
        if(adding): table.addTipo('string')
        handler.consumeToken()
    else:
        tree.addChild(exp_mat(handler, err, table))
        if(adding): table.addTipo('real')
    return tree

def exp_logica(handler, err, table):
    tree = TokenTree(Token(60, "TEXPLOGICA", "", False, getToken(handler, err).getLinha()))
    tree.addChild(exp_mat(handler, err, table))
    tree.addChild(exp_logica2(handler, err, table))
    return tree

def exp_logica2(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(61, "TEXPLOGICA2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TRELATIONAL):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err, table))
    return tree

def comandos2(handler, err, table):
    tk=getToken(handler, err)
    tree = TokenTree(Token(55, "TCOMANDOS2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPONTOEVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(comandos(handler, err, table))
    return tree

'''
def valor(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(59, "TCONSTVALOR", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(valor2(handler, err, table)) #não teria que ser nome2??
    elif(tk.getTokenCode() == TNUM):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat2(handler, err, table))
    elif(tk.getTokenCode() == TABREPARENTESES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat3(handler, err, table))
    else:
        err.addErr("identificador, numero, (", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def valor2(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TVALOR2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TABREPARENTESES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(parametro(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHAPARENTESES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
    else:
        tree.addChild(exp_mat2(handler, err, table))
    return tree
'''
def parametro(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(62, "TPARAMETRO", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TNUM):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(parametro2(handler, err, table))
    elif(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome2(handler, err, table))
        tree.addChild(parametro2(handler, err, table))
    return tree

def parametro2(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(63, "TPARAMETRO2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(parametro(handler, err, table))
    return tree

def exp_mat(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(64, "TEXPMAT", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TNUM):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat2(handler, err, table))
    elif(tk.getTokenCode() == TABREPARENTESES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat3())
    else:
        tree.addChild(nome_num(handler, err, table))
        tree.addChild(exp_mat4(handler, err, table))
    return tree

def exp_mat4(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(67, "TEXPMAT4", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TOPERATOR):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat(handler, err, table))
    return tree

def exp_mat2(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(65, "TEXPMAT2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TOPERATOR):
        tree.addChild(TokenTree(tk))
        hamdler.consumeToken()
        tree.addChild(exp_mat(handler, err, table))
    return tree

def exp_mat3(handler, err, table):
    tree = TokenTree(Token(66, "TEXPMAT3", "", False, getToken(handler, err).getLinha()))
    tree.addChild(nome_num(handler, err, table))
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TOPERATOR):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHAPARENTESES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    else:
        err.addErr("operador", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def nome_num(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(68, "TNOMENUM", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TNUM):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
    elif(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome3(handler, err, table))
    else:
        err.addErr("numero, identificador", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def nome3(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(69, "TNOME3", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TABREPARENTESES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(parametro(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHAPARENTESES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    else:
        tree.addChild(nome2(handler, err, table))
    return tree

def nome(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(70, "TNOME", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome2(handler, err, table))
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
        tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree

def nome2(handler, err, table):
    tk = getToken(handler, err)
    tree = TokenTree(Token(71, "TNOME2", "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPONTO):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome(handler, err, table))
    elif(tk.getTokenCode() == TABRECOLCHETES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome_num(handler, err, table))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHACOLCHETES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr("]", tk.getSymbol(), tk.getLinha(), 2)
            tk = panicMode(handler, err, tree.getRoot(), tk)
    return tree