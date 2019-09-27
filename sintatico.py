from token import *
from seeker import Handler



#Constantes para os token codes
TPROGRAMA = 1
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

'''

'''
class TokenTree:

    def __init__(self, node):
        self.node = node
        self.children = []

    def addChild(self, child):
        if((child.node.isTerminal) or (child.hasChildren())):
            self.children.append(child)
    
    def hasChildren(self):
        return (len(self.children) > 0)

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

#quando encontrar um terminal que você estava procurando, chamar handler.consumeToken()
def programa(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TPROGRAMA",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPROGRAMA):
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
                tree.addChild(Corpo(handler, err))
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr("program", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def Corpo(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TCORPO",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TCONST):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(constantes(handler, err))
    tree.addChild(Corpo2(handler, err))
    return tree

def Corpo2(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TCORPO2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TTYPE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(tipos(handler, err))
    tree.addChild(Corpo3(handler, err))
    return tree

def Corpo3(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TCORPO3",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVAR):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(variaveis(handler, err))
    tree.addChild(Corpo4(handler, err))
    return tree

def Corpo4(handler, err):
    tree = TokenTree(Token("TCORPO4",0, "", False, getToken(handler, err).getLinha()))
    tree.addChild(def_rotinas(handler, err))
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TBEGIN):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(comandos(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TEND):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            print("End")
        else:
            err.addErr("end", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr("begin", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def def_rotinas(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TDEFROTINAS",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TFUNCTION):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome_rotina(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TDOISPONTOS):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(tipo_dado(handler, err))
            tree.addChild(bloco_rotina(handler, err))
            tree.addChild(def_rotinas(handler, err))
        else:
            err.addErr(":", tk.getSymbol(), tk.getLinha(), 2)
    elif(tk.getTokenCode() == TPROCEDURE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome_rotina(handler, err))
        tree.addChild(bloco_rotina(handler, err))
        tree.addChild(def_rotinas(handler, err))
    return tree

def nome_rotina(handler, err):
    tk= getToken(handler, err)
    tree = TokenTree(Token("TPROGRAMA",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TABREPARENTESES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(variaveis(handler, err))
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TFECHAPARENTESES):
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
            else:
                err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr("(", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def bloco_rotina(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TBLOCO_ROTINA",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVAR):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(variaveis(handler, err))
        tk = getToken(handler, err)
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(bloco_rotina2(handler, err))
    else:
        tree.addChild(bloco(handler, err))
    return tree

def bloco_rotina2(handler, err):
    tk=getToken(handler, err)
    tree = TokenTree(Token("TBLOCO_ROTINA2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(lista_id3(handler, err))
    elif(tk.getTokenCode() == TDOISPONTOS):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(lista_id4(handler, err))
    tree.addChild(nome2(handler, err))
    tk = getToken(handler, err)
    if(tk.getTokenCode()==TATRIBUICAO):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(valor(handler, err))
        tk=getToken(handler, err)
        if(tk.getTokenCode()== TPONTOEVIRGULA):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr(":=", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def constantes(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TCONSTANTES",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol() == "="):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(const_valor(handler, err))
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
                tree.addChild(constantes2(handler, err))
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr("=", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def constantes2(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TCONSTANTES2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode()==TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(constantes3(handler, err))
    return tree

def constantes3(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TCONSTANTES3",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol()=="="):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(const_valor(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TDOISPONTOS):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(constantes2(handler, err))
    return tree
    
def tipos(handler, err):
    tk=getToken(handler, err)
    tree = TokenTree(Token("TTIPOS",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol()=="="):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(tipo_dado(handler, err))
            tree.addChild(tipos2(handler, err))
    return tree

def tipos2(handler, err):
    tk=getToken(handler, err)
    tree = TokenTree(Token("TTIPOS",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPONTOEVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(tipos(handler, err))
    return tree

def tipo_dado(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TTIPO_DADO",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TINTEGER):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
    if(tk.getTokenCode() == TREAL):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
    if(tk.getTokenCode() == TARRAY):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TABRECOLCHETES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TNUM):
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
                tk = getToken(handler, err)
                if(tk.getTokenCode() == TFECHACOLCHETES):
                    tree.addChild(TokenTree(tk))
                    handler.consumeToken()
                    tk = getToken(handler, err)
                    if(tk.getTokenCode() == TOF):
                        tree.addChild(TokenTree(tk))
                        handler.consumeToken()
                        tree.addChild(tipo_dado(handler, err))
                    else:
                        err.addErr("of", tk.getSymbol(), tk.getLinha(), 2)
                else:
                    err.addErr("]", tk.getSymbol(), tk.getLinha(), 2)
            else:
                err.addErr("numero", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr("[", tk.getSymbol(), tk.getLinha(), 2)
    if(tk.getTokenCode() == TRECORD):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(variaveis(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TEND):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr("end", tk.getSymbol(), tk.getLinha(), 2)
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
    return tree

def variaveis(handler, err):
    tree = TokenTree(Token("TVARIAVEIS",0, "", False, getToken(handler, err).getLinha()))
    tree.addChild(lista_id(handler, err))
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TDOISPONTOS):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(tipo_dado(handler, err))
        tree.addChild(variaveis2(handler, err))
    else:
        err.addErr(":", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def variaveis2(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TVARIAVEIS2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPONTOEVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(variaveis(handler, err))
    return tree

def lista_id(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TLISTA_ID",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(lista_id2(handler, err))
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def lista_id2(handler,err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TLISTA_ID2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(lista_id(handler, err))
    return tree

def lista_id3(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TLISTA_ID3",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(variaveis(handler, err))
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def lista_id4(hander, err):
    tree = TokenTree(Token("TPROGRAMA",0, "", False, getToken(handler, err).getLinha()))
    tree.addChild(tipo_dado(handler, err))
    tree.addChild(variaveis2(handler, err))
    return tree
                    
def comandos(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TCOMANDOS",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TWHILE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err))
        tree.addChild(bloco(handler, err))
        tree.addChild(comandos2(handler, err))
    elif(tk.getTokenCode() == TIF):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TTHEN):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(bloco(handler, err))
            tree.addChild(felse(handler, err))
            tree.addChild(comandos2(handler, err))
        else:
            err.addErr("then", tk.getSymbol, tk.getLinha(), 2)
    elif(tk.getTokenCode() == TWRITE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(const_valor(handler, err))
        tree.addChild(comandos2(handler, err))
    elif(tk.getTokenCode() == TREAD):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome(handler, err))
        tree.addChild(comandos2(handler, err))
    elif(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome2(handler, err))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TATRIBUICAO):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(exp_mat(handler, err))
            tree.addChild(comandos2(handler, err))
        else:
            err.addErr(":=", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def bloco(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TBLOCO",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TBEGIN):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(comandos(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode()==TEND):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr("end", tk.getSymbol(), tk.getLinha(), 2)
    else:
        tree.addChild(comandos3(handler, err))
    return tree

def comandos3(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TCOMANDOS3",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TWHILE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err))
        tree.addChild(bloco(handler, err))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
    elif(tk.getTokenCode() == TIF):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TTHEN):
            tree.addChild(TokenTree(tk))
            tk.consumeToken()
            tree.addChild(bloco(handler, err))
            tree.addChild(felse(handler, err))
            tk=getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr("then", tk.getSymbol, tk.getLinha(), 2)
    elif(tk.getTokenCode() == TWRITE):
        tree.addChild(TokenTree(tk))
        tk.consumeToken()
        tree.addChild(const_valor(handler, err))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
    elif(tk.getTokenCode() == TREAD):
        tree.addChild(TokenTree(tk))
        tk.consumeToken()
        tree.addChild(nome(handler, err))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
    elif(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome2(handler, err))
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TATRIBUICAO):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
            tree.addChild(exp_mat(handler, err))
            tk=getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                tree.addChild(TokenTree(tk))
                handler.consumeToken()
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr(":=", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def felse(handler, err):
    tk=getToken(handler, err)
    tree = TokenTree(Token("TELSE",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TELSE):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(bloco(handler, err))
    return tree

def const_valor(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TCONST_VALOR",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TSTRING):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
    else:
        tree.addChild(exp_mat(handler, err))
    return tree

def exp_logica(handler, err):
    tree = TokenTree(Token("TEXP_LOGICA",0, "", False, getToken(handler, err).getLinha()))
    tree.addChild(exp_mat(handler, err))
    tree.addChild(exp_logica2(handler, err))
    return tree

def exp_logica2(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TEXP_LOGICA2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TRELATIONAL):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_logica(handler, err))
    return tree

def comandos2(handler, err):
    tk=getToken(handler, err)
    tree = TokenTree(Token("TCOMANDOS2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPONTOEVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(comandos(handler, err))
    return tree

def valor(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TVALOR",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(valor2(handler, err))
    elif(tk.getTokenCode() == TNUM):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat2(handler, err))
    elif(tk.getTokenCode() == TABREPARENTESES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat3(handler, err))
    else:
        err.addErr("identificador, numero, (", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def valor2(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TVALOR2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TABREPARENTESES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(parametro(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHAPARENTESES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
    else:
        tree.addChild(exp_mat2(handler, err))
    return tree

def parametro(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TPARAMETRO",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TNUM):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(parametro2(handler, err))
    elif(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome2(handler, err))
        tree.addChild(parametro2(handler, err))
    return tree

def parametro2(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TÀRAMETRO2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TVIRGULA):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(parametro(handler, err))
    return tree

def exp_mat(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TEXP_MAT",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TNUM):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat2(handler, err))
    elif(tk.getTokenCode() == TABREPARENTESES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat3())
    else:
        tree.addChild(nome_num(handler, err))
        tree.addChild(exp_mat4(handler, err))
    return tree

def exp_mat4(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TEXP_MAT4",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TOPERATOR):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat(handler, err))
    return tree

def exp_mat2(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TEXP_MAT2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TOPERATOR):
        tree.addChild(TokenTree(tk))
        hamdler.consumeToken()
        tree.addChild(exp_mat(handler, err))
    return tree

def exp_mat3(handler, err):
    tree = TokenTree(Token("TPROGRAMA",0, "", False, getToken(handler, err).getLinha()))
    tree.addChild(nome_num(handler, err))
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TOPERATOR):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(exp_mat(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHAPARENTESES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr("operador", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def nome_num(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TNOME_NUM",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TNUM):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
    elif(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome3(handler, err))
    else:
        err.addErr("numero, identificador", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def nome3(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TNOME3",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TABREPARENTESES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(parametro(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHAPARENTESES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
    else:
        tree.addChild(nome2(handler, err))
    return tree

def nome(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TNOME",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TID):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome2(handler, err))
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)
    return tree

def nome2(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TNOME2",0, "", False, tk.getLinha()))
    if(tk.getTokenCode() == TPONTO):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome(handler, err))
    elif(tk.getTokenCode() == TABRECOLCHETES):
        tree.addChild(TokenTree(tk))
        handler.consumeToken()
        tree.addChild(nome_num(handler, err))
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHACOLCHETES):
            tree.addChild(TokenTree(tk))
            handler.consumeToken()
        else:
            err.addErr("]", tk.getSymbol(), tk.getLinha(), 2)
    return tree