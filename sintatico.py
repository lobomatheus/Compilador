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

    def __init__(self, node, children=[]):

        self.node = node
        self.children = children

    def addChild(self, child):

        self.children.append(child)

# usa essa função aqui pra pegar o próximo token
def getToken(handler, err):
    tkn = handler.getToken()
    if(tkn.getTokenCode() == -1):
        err.addErr(tkn.getSymbol(), "TError", tkn.getLinha(), 1)
    tkn.exhibit()
    return tkn

#quando encontrar um terminal que você estava procurando, chamar handler.consumeToken()
def programa(handler, err):
    tk = getToken(handler, err)
    tree = TokenTree(Token("TPROGRAMA", "", False, tk.getLinha()))
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

def Corpo(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TCONST):
        handler.consumeToken()
        constantes(handler, err)
    Corpo2(handler, err)

def Corpo2(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TTYPE):
        handler.consumeToken()
        tipos(handler, err)
    Corpo3(handler, err)

def Corpo3(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TVAR):
        handler.consumeToken()
        variaveis(handler, err)
    Corpo4(handler, err)

def Corpo4(handler, err):
    def_rotinas(handler, err)
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TBEGIN):
        handler.consumeToken()
        comandos(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TEND):
            handler.consumeToken()
            print("End")
        else:
            err.addErr("end", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr("begin", tk.getSymbol(), tk.getLinha(), 2)

def def_rotinas(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TFUNCTION):
        handler.consumeToken()
        nome_rotina(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TDOISPONTOS):
            handler.consumeToken()
            tipo_dado(handler, err)
            bloco_rotina(handler, err)
            def_rotinas(handler, err)
        else:
            err.addErr(":", tk.getSymbol(), tk.getLinha(), 2)
    elif(tk.getTokenCode() == TPROCEDURE):
        handler.consumeToken()
        nome_rotina(handler, err)
        bloco_rotina(handler, err)
        def_rotinas(handler, err)

def nome_rotina(handler, err):
    tk= getToken(handler, err)
    if(tk.getTokenCode() == TID):
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TABREPARENTESES):
            handler.consumeToken()
            variaveis(handler, err)
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TFECHAPARENTESES):
                handler.consumeToken()
            else:
                err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr("(", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)

def bloco_rotina(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TVAR):
        handler.consumeToken()
        variaveis(handler, err)
        tk = getToken(handler, err)
    if(tk.getTokenCode() == TID):
        handler.consumeToken()
        bloco_rotina2(handler, err)
    else:
        bloco(handler, err)

def bloco_rotina2(handler, err):
    tk=getToken(handler, err)
    if(tk.getTokenCode() == TVIRGULA):
        handler.consumeToken()
        lista_id3(handler, err)
    elif(tk.getTokenCode() == TDOISPONTOS):
        handler.consumeToken()
        lista_id4(handler, err)
    nome2(handler, err)
    tk = getToken(handler, err)
    if(tk.getTokenCode()==TATRIBUICAO):
        handler.consumeToken()
        valor(handler, err)
        tk=getToken(handler, err)
        if(tk.getTokenCode()== TPONTOEVIRGULA):
            handler.consumeToken()
        else:
            err.addErr(":", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr(":=", tk.getSymbol(), tk.getLinha(), 2)

def constantes(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TID):
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol() == "="):
            handler.consumeToken()
            const_valor(handler, err)
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                handler.consumeToken()
                constantes2(handler, err)

def constantes2(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode()==TID):
        handler.consumeToken()
        constantes3(handler, err)

def constantes3(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol()=="="):
        handler.consumeToken()
        const_valor(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TDOISPONTOS):
            handler.consumeToken()
            constantes2(handler, err)
    
def tipos(handler, err):
    tk=getToken(handler, err)
    if(tk.getTokenCode() == TID):
        handler.consumeToken()
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol()=="="):
            handler.consumeToken()
            tipo_dado(handler, err)
            tipos2(handler, err)

def tipos2(handler, err):
    tk=getToken(handler, err)
    if(tk.getTokenCode() == TPONTOEVIRGULA):
        handler.consumeToken()
        tipos(handler, err)

def tipo_dado(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TINTEGER):
        handler.consumeToken()
    if(tk.getTokenCode() == TREAL):
        handler.consumeToken()
    if(tk.getTokenCode() == TARRAY):
        handler.consumeToken()
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TABRECOLCHETES):
            handler.consumeToken()
            tk = getToken(handler, err)
            if(tk.getTokenCode() == TNUM):
                handler.consumeToken()
                tk = getToken(handler, err)
                if(tk.getTokenCode() == TFECHACOLCHETES):
                    handler.consumeToken()
                    tk = getToken(handler, err)
                    if(tk.getTokenCode() == TOF):
                        handler.consumeToken()
                        tipo_dado(handler, err)
                    else:
                        err.addErr("of", tk.getSymbol(), tk.getLinha(), 2)
                else:
                    err.addErr("]", tk.getSymbol(), tk.getLinha(), 2)
            else:
                err.addErr("numero", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr("[", tk.getSymbol(), tk.getLinha(), 2)
    if(tk.getTokenCode() == TRECORD):
        handler.consumeToken()
        variaveis(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TEND):
            handler.consumeToken()
        else:
            err.addErr("end", tk.getSymbol(), tk.getLinha(), 2)
    if(tk.getTokenCode() == TID):
        handler.consumeToken()

def variaveis(handler, err):
    lista_id(handler, err)
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TDOISPONTOS):
        handler.consumeToken()
        tipo_dado(handler, err)
        variaveis2(handler, err)
    else:
        err.addErr(":", tk.getSymbol(), tk.getLinha(), 2)

def variaveis2(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TPONTOEVIRGULA):
        handler.consumeToken()
        variaveis(handler, err)

def lista_id(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TID):
        handler.consumeToken()
        lista_id2(handler, err)
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)

def lista_id2(handler,err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TVIRGULA):
        handler.consumeToken()
        lista_id(handler, err)

def lista_id3(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TID):
        handler.consumeToken()
        variaveis(handler, err)
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)

def lista_id4(hander, err):
    tipo_dado(handler, err)
    variaveis2(handler, err)
                    
def comandos(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TWHILE):
        handler.consumeToken()
        exp_logica(handler, err)
        bloco(handler, err)
        comandos2(handler, err)
    elif(tk.getTokenCode() == TIF):
        handler.consumeToken()
        exp_logica(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TTHEN):
            handler.consumeToken()
            bloco(handler, err)
            felse(handler, err)
            comandos2(handler, err)
        else:
            err.addErr("then", tk.getSymbol, tk.getLinha(), 2)
    elif(tk.getTokenCode() == TWRITE):
        handler.consumeToken()
        const_valor(handler, err)
        comandos2(handler, err)
    elif(tk.getTokenCode() == TREAD):
        handler.consumeToken()
        nome(handler, err)
        comandos2(handler, err)
    elif(tk.getTokenCode() == TID):
        handler.consumeToken()
        nome2(handler, err)
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TATRIBUICAO):
            handler.consumeToken()
            exp_mat(handler, err)
            comandos2(handler, err)
        else:
            err.addErr(":=", tk.getSymbol(), tk.getLinha(), 2)

def bloco(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TBEGIN):
        handler.consumeToken()
        comandos(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode()==TEND):
            handler.consumeToken()
        else:
            err.addErr("end", tk.getSymbol(), tk.getLinha(), 2)
    else:
        comandos3(handler, err)

def comandos3(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TWHILE):
        handler.consumeToken()
        exp_logica(handler, err)
        bloco(handler, err)
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
    elif(tk.getTokenCode() == TIF):
        handler.consumeToken()
        exp_logica(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TTHEN):
            tk.consumeToken()
            bloco(handler, err)
            felse(handler, err)
            tk=getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                handler.consumeToken()
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr("then", tk.getSymbol, tk.getLinha(), 2)
    elif(tk.getTokenCode() == TWRITE):
        tk.consumeToken()
        const_valor(handler, err)
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
    elif(tk.getTokenCode() == TREAD):
        tk.consumeToken()
        nome(handler, err)
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TPONTOEVIRGULA):
            handler.consumeToken()
        else:
            err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
    elif(tk.getTokenCode() == TID):
        handler.consumeToken()
        nome2(handler, err)
        tk=getToken(handler, err)
        if(tk.getTokenCode() == TATRIBUICAO):
            handler.consumeToken()
            exp_mat(handler, err)
            tk=getToken(handler, err)
            if(tk.getTokenCode() == TPONTOEVIRGULA):
                handler.consumeToken()
            else:
                err.addErr(";", tk.getSymbol(), tk.getLinha(), 2)
        else:
            err.addErr(":=", tk.getSymbol(), tk.getLinha(), 2)

def felse(handler, err):
    tk=getToken(handler, err)
    if(tk.getTokenCode() == TELSE):
        handler.consumeToken()
        bloco(handler, err)

def const_valor(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TSTRING):
        handler.consumeToken()
    else:
        exp_mat(handler, err)

def exp_logica(handler, err):
    exp_mat(handler, err)
    exp_logica2(handler, err)

def exp_logica2(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TRELATIONAL):
        handler.consumeToken()
        exp_logica(handler, err)

def comandos2(handler, err):
    tk=getToken(handler, err)
    if(tk.getTokenCode() == TPONTOEVIRGULA):
        handler.consumeToken()
        comandos(handler, err)

def valor(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TID):
        handler.consumeToken()
        valor2(handler, err)
    elif(tk.getTokenCode() == TNUM):
        handler.consumeToken()
        exp_mat2(handler, err)
    elif(tk.getTokenCode() == TABREPARENTESES):
        handler.consumeToken()
        exp_mat3(handler, err)
    else:
        err.addErr("identificador, numero, (", tk.getSymbol(), tk.getLinha(), 2)

def valor2(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TABREPARENTESES):
        handler.consumeToken()
        parametro(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHAPARENTESES):
            handler.consumeToken()
        else:
            err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
    else:
        exp_mat2(handler, err)

def parametro(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TNUM):
        handler.consumeToken()
        parametro2(handler, err)
    elif(tk.getTokenCode() == TID):
        handler.consumeToken()
        nome2(handler, err)
        parametro2(handler, err)

def parametro2(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TVIRGULA):
        handler.consumeToken()
        parametro(handler, err)

def exp_mat(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TNUM):
        handler.consumeToken()
        exp_mat2(handler, err)
    elif(tk.getTokenCode() == TABREPARENTESES):
        handler.consumeToken()
        exp_mat3()
    else:
        nome_num(handler, err)
        exp_mat4(handler, err)

def exp_mat4(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TOPERATOR):
        handler.consumeToken()
        exp_mat(handler, err)

def exp_mat2(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TOPERATOR):
        hamdler.consumeToken()
        exp_mat(handler, err)

def exp_mat3(handler, err):
    nome_num(handler, err)
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TOPERATOR):
        handler.consumeToken()
        exp_mat(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHAPARENTESES):
            handler.consumeToken()
        else:
            err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
    else:
        err.addErr("operador", tk.getSymbol(), tk.getLinha(), 2)

def nome_num(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TNUM):
        handler.consumeToken()
    elif(tk.getTokenCode() == TID):
        handler.consumeToken()
        nome3(handler, err)
    else:
        err.addErr("numero, identificador", tk.getSymbol(), tk.getLinha(), 2)

def nome3(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TABREPARENTESES):
        handler.consumeToken()
        parametro(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHAPARENTESES):
            handler.consumeToken()
        else:
            err.addErr(")", tk.getSymbol(), tk.getLinha(), 2)
    else:
        nome2(handler, err)

def nome(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TID):
        handler.consumeToken()
        nome2(handler, err)
    else:
        err.addErr("identificador", tk.getSymbol(), tk.getLinha(), 2)

def nome2(handler, err):
    tk = getToken(handler, err)
    if(tk.getTokenCode() == TPONTO):
        handler.consumeToken()
        nome(handler, err)
    elif(tk.getTokenCode() == TABRECOLCHETES):
        handler.consumeToken()
        nome_num(handler, err)
        tk = getToken(handler, err)
        if(tk.getTokenCode() == TFECHACOLCHETES):
            handler.consumeToken()
        else:
            err.addErr("]", tk.getSymbol(), tk.getLinha(), 2)