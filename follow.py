from token import *

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

#nao terminais
TCORPO = 34
TCORPO2 = 35
TCORPO3 = 36
TCORPO4 = 37
TDEFROTINAS = 38
TNOMEROTINA = 39
TBLOCOROTINA = 40
TBLOCOROTINA2 = 41
TLISTAID3 = 42
TLISTAID4 = 43
TCONSTANTES = 44
TCONSTANTES2 = 45
TCONSTANTES3 = 46
TTIPOS = 47
TTIPOS2 = 48
TTIPODADO = 49
TVARIAVEIS = 50
TVARIAVEIS2 = 51
TLISTAID = 52
TLISTAID2 = 53
TCOMANDOS = 54
TCOMANDOS2 = 55
TCOMANDOS3 = 56
TBLOCO = 57
TELSE = 58
TCONSTVALOR = 59
TEXPLOGICA = 60
TEXPLOGICA2 = 61
TPARAMETRO = 62
TPARAMETRO2 = 63
TEXPMAT = 64
TEXPMAT2 = 65
TEXPMAT3 = 66
TEXPMAT4 = 67
TNOMENUM = 68
TNOME3 = 69
TNOME = 70
TNOME2 = 71
TPROGRAMA = 72

lista_follows = [
    [None] , #EOF
    [TBEGIN],
    [TDOISPONTOS , TID , TBEGIN , TWHILE , TIF , TWRITE , TREAD],
    [TFUNCTION, TPROCEDURE, TBEGIN],
    [TTYPE, TVAR, TFUNCTION, TPROCEDURE, TBEGIN],
    [TVAR, TFUNCTION, TPROCEDURE, TBEGIN],
    [TID, TBEGIN, TWHILE, TIF, TWRITE, TREAD, TPONTOEVIRGULA, TVAR, TFUNCTION, TPROCEDURE, TFECHAPARENTESES, TEND],
    [TFUNCTION, TPROCEDURE, TBEGIN, TFECHAPARENTESES, TEND],
    [TDOISPONTOS],
    [TEND],
    [TFUNCTION, TPROCEDURE, TBEGIN, TPONTOEVIRGULA, TEND, TELSE],
    [TPONTOEVIRGULA, TEND],
    [TBEGIN, TWHILE, TIF, TWRITE, TREAD, TID, TTHEN],
    [TFECHAPARENTESES],
    [TPONTOEVIRGULA, TEND, TOPERATOR, TRELATIONAL, TBEGIN, TWHILE, TIF, TWRITE, TREAD, TID, TTHEN, TFECHAPARENTESES],
    [TFECHACOLCHETES, TOPERATOR],
    [TPONTOEVIRGULA, TEND, TOPERATOR, TRELATIONAL, TBEGIN, TWHILE, TIF, TWRITE, TREAD, TID, TTHEN, TFECHAPARENTESES, TATRIBUICAO, TVIRGULA, TFECHACOLCHETES],
]

def getFollowsArray(tkn):
    if (tkn.getTokenCode() in [34, 35, 36, 37, 72]):
        return lista_follows[0]
    elif (tkn.getTokenCode() in [38]):
        return lista_follows[1]
    elif (tkn.getTokenCode() in [39]):
        return lista_follows[2]
    elif (tkn.getTokenCode() in [40, 41, 42, 43]):
        return lista_follows[3]
    elif (tkn.getTokenCode() in [44, 45, 46]):
        return lista_follows[4]
    elif (tkn.getTokenCode() in [47, 48]):
        return lista_follows[5] 
    elif (tkn.getTokenCode() in [49]):
        return lista_follows[6]
    elif (tkn.getTokenCode() in [50, 51]):
        return lista_follows[7]
    elif (tkn.getTokenCode() in [52, 53]):
        return lista_follows[8]
    elif (tkn.getTokenCode() in [54, 55]):
        return lista_follows[9]
    elif (tkn.getTokenCode() in [56, 57]):
        return lista_follows[10]
    elif (tkn.getTokenCode() in [58, 59]):
        return lista_follows[11]
    elif (tkn.getTokenCode() in [60, 61]):
        return lista_follows[12]
    elif (tkn.getTokenCode() in [62, 63]):
        return lista_follows[13]
    elif (tkn.getTokenCode() in [64, 65, 66, 67]):
        return lista_follows[14]
    elif (tkn.getTokenCode() in [68, 69]):
        return lista_follows[15]
    elif (tkn.getTokenCode() in [70, 71]):
        return lista_follows[16]
    