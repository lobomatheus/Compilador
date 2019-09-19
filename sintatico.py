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
def getToken(handler):
    ret = handler.nextToken()
    if(ret == "$"):
        tkn = Token(-1, "", "", False)
        print("eof")
    else:
        tkn = matchToken(ret)
    tkn.exhibit()
    return tkn



def Corpo(handler):
    tk = getToken(handler)
    if(tk.getTokenCode() == TCONST):
        cosntantes(handler)
    Corpo2(handler)

def Corpo2(handler):
    tk = getToken(handler)
    if(tk.getTokenCode() == TTYPE):
        tipos(handler)
    Corpo3(handler)

def Corpo3(handler):
    tk = getToken(handler)
    if(tk.getTokenCode() == TVAR):
        variaveis(handler)
    Corpo4(handler)

def Corpo4(handler):
    def_rotinas(handler)
    tk = getToken(handler)
    if(tk.getTokenCode() == TBEGIN):
        comandos(handler)
        tk getToken(handler)
        if(tk.getTokenCode() == TEND):
            print("End")
        else:
            print("Error corpo4 end")
    else:
        print("Error corpo4 begin")

def def_rotinas(handler):
    tk = getToken(handler)
    if(tk.getTokenCode() == TFUNCTION):
        nome_rotina(handler)
        tk = getToken(handler)
        if(tk.getTokenCode() == TDOISPONTOS):
            tipo_dado(handler)
            bloco_rotina(handler)
            def_rotinas(handler)
        else:
            print("error dois pontos def_rotinas")
    elif(tk.getTokenCode() == TPROCEDURE):
        nome_rotina(handler)
        bloco_rotina(handler)
        def_rotinas(handler)
    else:
        #o que aconteceria aqui? Ele já pegou o token begin e quando voltar não estará mais nele
        return

def nome_rotina(handler):
    tk= getToken(handler)
    if(tk.getTokenCode() == TID):
        tk = getToken(handler)
        if(tk.getTokenCode() == TOPERATOR):
            variaveis(handler)
        else:
            print("error parenteses nome_rotina")
    else:
        print("error id nome_rotina")

def bloco_rotina(handler):
    tk = getToken(handler)
    if(tk.getTokenCode() == TID):
        bloco_rotina2(handler)
    else:
        bloco(handler)

def bloco_rotina2(handler):
    tk=getToken(handler)
    if(tk.getTokenCode() == TVIRGULA):
        lista_id3(handler)
    elif(tk.getTokenCode() == TDOISPONTOS):
        lista_id4(handler)
    #já pegou o token que teria que ter sido enviado para nome2
    nome2(handler)
    tk = getToken(handler)
    if(tk.getTokenCode()==TATRIBUICAO):
        valor(handler)
        tk=getToken(handler)
        if(tk.getTokenCode()== TPONTOEVIRGULA):
            return
        else:
            print("error: bloco_rotina2 ponto e virgula")
    else:
        print("error: bloco_rotina2 atribuicao")

def constantes(handler):
    tk = getToken(handler)
    if(tk.getTokenCode() == TID):
        tk = getToken(handler)
        if(tk.getTokenCode() == TRELATIONAL and tk.getSymbol() == "="):
            const_valor(handler)
            tk = getToken(handler)
            if(tk.getTokenCode() == TDOISPONTOS):
                constantes2(handler)

def constantes2(handler):
    

