# -*- coding: utf-8 -*-

#tabela de símbolos

class TypeTable:
    def __init__(self):
        self.table = []
    
    def addType(self, tp, numElem=0):
        if(numElem == 0): self.table.add([tp])
        else: self.table.add([tp, numElem])

class SymbolTable:
    def __init__(self):
        self.table = []
        self.atual = None
        self.buildMode = False
        self.paramMode = False
        self.recordMode = False
        self.escopo=[]
        self.arrayCount = 0
        self.idEsquerda = None
        self.escopoEsquerda = None
        self.idDireita=None 
        self.escopoDireita=None
        self.verificandoDireita=False 
        self.verificandoEsquerda=False
        self.pauseTipos=True
        self.direitaArray=False 
        self.esquerdaArray=False
        self.confere = False

        self.paramTk=None 
        self.paramEscopo=None

        #-------------------
        self.verPar=False
        self.paramNum=0
        self.paramFunc=None
        self.function = None
        #-------------------

    
    def printTable(self):
        for s in self.table:
            print(s)
    
    # id: identificador do símbolo
    # classe: variavel, função, procedure
    # type: tipo do símbolo (tipo de retorno da função ou tipo da variavel)
    # scope: escopo global ou função onde foi declarado
    def newSymbol(self, classe):
        self.buildMode = True
        self.atual = {
            'id' : [],
            'classe' : classe,
            'tipo' : '',
            'escopo' : self.peekEscopo()
        }
        if(classe == 'procedure'): self.atual['tipo'] = 'void'

    def addName(self, name):
        self.atual['id'].append(name)
        #print(self.atual['id'])

    def addTipo(self, tipo):
        self.atual['tipo'] = tipo

    """ def addSymbol(self, id, classe, tp):
        self.atual = [id, classe, tp, scope]
        if(classe == 1):
            #adicionar coisas de variavel
        elif(classe == 2):
            #adicionar coisas de funcao
        elif(classe == 3):
            #adicinoar coisas de procedure """

    def addElemNum(self, nElem):
        self.atual['nElem'] = nElem
    
    def startParam(self):
        self.func = self.atual.copy()
        #print(self.atual)
        self.func['params'] = []
        self.paramMode = True
        self.addEscopo(self.atual['id'][0])
        self.atual = {
            'id' : [],
            'classe' : 'var',
            'tipo' : '',
            'escopo' : self.peekEscopo()
        }
    
    def stopParam(self):
        #print(self.func)
        self.atual = self.func.copy()
        self.func = []
        self.paramMode = False

    def mode(self):
        return self.buildMode

    def arrayNum(self):
        return "array" + str(self.arrayCount)

    def getName(self):
        return self.atual['id'][0]

    def test(self):
        print(self.atual)

    def saveSymbol(self):
        for id in self.atual['id']:
            new = [id, self.atual['classe'], self.atual['tipo'], self.atual['escopo']]
            if(self.atual['tipo'] == 'array'):
                new.append(self.atual['nElem'])
                self.arrayCount = self.arrayCount + 1
            #if(self.atual['tipo'] == 'record'): self.recordCount = self.recordCount + 1
            if(new[1] == 'function' or new[1] == 'procedure'):
                new.append(self.atual['params'])
            if(self.paramMode):self.func['params'].append(new)
            else: 
                self.table.append(new)
                if(new[1] == 'function'):
                    self.table.append(['result', 'var', new[2], new[0]])

        self.atual = None

    def findSymbol(self, id, tp=None):
        return False

    #-----Funcoes da pilha
    def addEscopo(self, scope):
        self.escopo.append(scope)

    def rmEscopo(self):
        self.escopo.pop()
    
    def peekEscopo(self):
        if(self.escopo == []): return 'global'
        else: return self.escopo[len(self.escopo)-1]

    #------Funcoes de verificacao
    def mesmoNome(self, tk, err):
        escopoAtual = self.peekEscopo()
        id = tk.getSymbol()
        if(len(list(filter((lambda x: x[0] == id and x[3] == escopoAtual), self.table))) > 0):
            err.addErr(tk.getSymbol(), tk, tk.getLinha(), 4)
            #return True
        if(self.atual != None):
            for n in self.atual['id']:
                if(n == id):
                    err.addErr(tk.getSymbol(), tk, tk.getLinha(), 4)
        if(escopoAtual != 'global'):
            funcs = list(filter((lambda x: x[0]==escopoAtual and (x[1]=='function'or x[1]=='procedure')),self.table))
            if(len(funcs) > 0):
                params = funcs[0][4]
                for p in params:
                    if(p[0] == id):
                        err.addErr(tk.getSymbol(), tk, tk.getLinha(), 4)


        #else: return False

    #---------------------------

    def verificarFuncao(self, tk, err):
        id = tk.getSymbol()
        funcs = list(filter((lambda x: (x[1] == 'function' or x[1] == 'procedure') and x[0] == id), self.table))
        if(len(funcs) == 0):
            err.addErr(tk.getSymbol(), tk, tk.getLinha(), 6)
            return False
        return True


    #---------------------------provavelmente nao sera necessario (regra 1 cobre)
    """ def verificarCampoRegistro(self, idReg, idCampo):
        regis = list(filter((lambda x: x[4] == idReg and x[0]==idCampo)))
        if(lem(regs) == 0):
            return True
        return False """


    

    #-------------------------------------------------------------------------
    def iniciarVerTipoEsquerda(self, tk):
        self.idEsquerda = tk
        self.escopoEsquerda = self.peekEscopo()
        self.verificandoEsquerda = True
        self.pauseTipos=False
        

    def finalizarVerTipoEsquerda(self):
        self.verificandoEsquerda = False


    def iniciarVerTipoDireita(self):
        self.verificandoDireita = True
        self.pauseTipos=False


    def finalizarVerTipoDireita(self, err):
        
        tipo1 = self.getTipo(self.idEsquerda.getSymbol(), self.escopoEsquerda, self.esquerdaArray)

        print(self.idDireita)
        if(self.idDireita.getType()== 'TNum'):
            if tipo1 != 'int' and tipo1 != 'real':
                err.addErr(self.idDireita.getSymbol(), self.idDireita, self.idDireita.getLinha(), 10)
        else:
            tipo2 = self.getTipo(self.idDireita.getSymbol(), self.escopoDireita, self.direitaArray)
            if(tipo1 != tipo2):
                if(not(tipo1=='int' and tipo2=='real') and not(tipo2=='int' and tipo1=='real')):
                    err.addErr(self.idDireita.getSymbol(), self.idDireita, self.idDireita.getLinha(), 10)
        
        self.idEsquerda=None 
        self.idDireita=None 
        self.escopoDireita=None 
        self.escopoEsquerda=None
        self.verificandoDireita = False
        self.direitaArray=False
        self.esquerdaArray=False
        self.pauseTipos=True

    def verificarTipo(self, tk):
        if(self.pauseTipos):
            return
        if(self.verificandoEsquerda):
            self.idEsquerda = tk
            self.escopoEsquerda = self.peekEscopo()
        
        elif(self.verificandoDireita):
            self.idDireita = tk
            self.escopoDireita = self.peekEscopo()

    def getTipo(self, id, escopo, val=False):
        for s in self.table:
            if(s[0] == id and s[3]==escopo):
                return self.tratarTiposDefinidos(s[2], val)
        for s in self.table:
            if(s[0] == id and s[3]=='global'):
                return self.tratarTiposDefinidos(s[2], val)
        func = list(filter((lambda x: x[0]==escopo), self.table))
        if(len(func) > 0):
            if(func[0][1] == 'function' or func[0][1] == 'procedure'):
                for s in func[0][4]:
                    if(s[0] == id):
                        return self.tratarTiposDefinidos(s[2], val)
            else:
                return self.tratarTiposDefinidos(func[0][0], val)
        return ''
    
    def tratarTiposDefinidos(self, tipo, val):
        if(not(val)): tipos = list(filter((lambda x: (x[1]=='tipo') and x[0]==tipo), self.table))
        else: tipos = list(filter((lambda x: (x[1]=='tipo' or x[1]=='array') and x[0]==tipo), self.table))
        if(len(tipos) > 0):
            return self.tratarTiposDefinidos(tipos[0][2], val)
        else:
            return tipo



    def pauseVerTipos(self, val):
        self.pauseTipos = val
        if(self.idDireita): self.direitaArray=True
        elif(self.idEsquerda): self.esquerdaArray=True
        elif(self.verPar): self.paramVetor=True

    #-------------------------------------------------------------------------

    def verificarRegistro(self, tk, err):
        id = tk.getSymbol()
        escopoAtual = self.peekEscopo()
        #print(escopoAtual)
        #print(self.getRecords(escopoAtual))
        tipo = self.getTipo(id, escopoAtual)
        if(tipo != 'record'):
            print(tipo)
            err.addErr(tk.getSymbol(), tk, tk.getLinha(), 7)



    """         reg = list(filter((lambda x: (x[3] == escopoAtual and self.tratarTiposDefinidos(x[2]) =='record') and x[0] == id), self.table))
        print(reg)
        if(len(reg) == 0):
            reg = list(filter((lambda x: (x[3] == 'global' and self.tratarTiposDefinidos(x[2]) =='record') and x[0] == id), self.table))
            if(len(reg) == 0):
                if(escopoAtual != 'global'):
                    funcs = list(filter((lambda x: x[0]==escopoAtual and (x[1]=='function'or x[1]=='procedure')),self.table))
                    if(len(funcs) > 0):
                        params = funcs[0][4]
                        for p in params:
                            if(p[0] == id):
                                reg.append(p)
                #print(reg, tk.getLinha())
                if(len(reg)==0):
                    err.addErr(tk.getSymbol(), tk, tk.getLinha(), 7)"""
                        
    def getElements(self, classe, escopo):
        rec = list(filter((lambda x: (self.getTipo(x[0],escopo)==classe and x[3]==escopo)), self.table))
        rec2 = []
        for r in rec:
            rec2.append(r[0])
        return rec2

    def tratarTipoArray(self, tipo):
        tipos = list(filter((lambda x: (x[1]=='tipo' or x[1]=='array') and x[0]==tipo), self.table))
        if(len(tipos) > 0):
            if(tipos[0][1] != 'array'):
                return self.tratarTipoArray(tipos[0][2])
            else:
                return tipos[0][1]
        else:
            return tipo


    def verificarVetor(self, tk, err):
        id = tk.getSymbol()
        escopoAtual = self.peekEscopo()

        tipo = self.tratarTipoArray(self.getTipo2(id, escopoAtual))


        if(tipo != 'array'):
            #print(tipo)
            err.addErr(tk.getSymbol(), tk, tk.getLinha(), 5)



        """ reg = list(filter((lambda x: (x[3] == escopoAtual and x[0] in self.getElements('array', escopoAtual)) and x[0] == id), self.table))
        if(len(reg) == 0):
            reg = list(filter((lambda x: (x[3] == 'global' and x[0] in self.getElements('array', 'global')) and x[0] == id), self.table))
            if(len(reg) == 0):
                if(escopoAtual != 'global'):
                    funcs = list(filter((lambda x: x[0]==escopoAtual and (x[1]=='function'or x[1]=='procedure')),self.table))
                    if(len(funcs) > 0):
                        params = funcs[0][4]
                        for p in params:
                            if(p[0] == id):
                                reg.append(p)
                if(len(reg)==0):
                    err.addErr(tk.getSymbol(), tk, tk.getLinha(), 5) """
        

    def setVerificacao(self, estado):
        self.confere = estado

    def setRecordMode(self, estado):
        self.recordMode = estado

    def verificarDeclaracao(self, tk, err):
        escopoAtual = self.peekEscopo()
        if (self.confere == True):
            id = tk.getSymbol()
            dec = list(filter((lambda x: (x[3]==escopoAtual and x[0]==id)), self.table))
            if(len(dec)==0):
                dec = list(filter((lambda x: (x[3]=='global') and x[0]==id), self.table))
                if (len(dec) == 0):
                    if(escopoAtual != 'global'):
                        funcs = list(filter((lambda x: x[0]==escopoAtual and (x[1]=='function'or x[1]=='procedure')),self.table))
                        if(len(funcs) > 0):
                            params = funcs[0][4]
                            for p in params:
                                if(p[0] == id):
                                    dec.append(p)
                    if (len(dec) == 0):
                        err.addErr(tk.getSymbol(), tk, tk.getLinha(), 3)

    #---------------------------------
    #----------Verificação dos parametros

    def getParams(self, fId):
        return list(filter((lambda x: x[0]==fId and (x[1]=='function' or x[1]=='procedure')), self.table))[0][4]
    
    def tratarTiposDefinidos2(self, tipo, val):
        tipos = list(filter((lambda x: (x[1]=='array') and x[0]==tipo), self.table))
        if(len(tipos) > 0 and val):
            return self.tratarTiposDefinidos2(tipos[0][2], val)
        else:
            return tipo

    def getTipo2(self, id, escopo):
        for s in self.table:
            if(s[0] == id and s[3]==escopo):
                return s[2]
        for s in self.table:
            if(s[0] == id and s[3]=='global'):
                return s[2]
        func = list(filter((lambda x: x[0]==escopo), self.table))
        if(len(func) > 0):
            for s in func[0][4]:
                if(s[0] == id):
                    return s[2]
        return ''

    def inicarVerificacaoParametros(self, tk):
        self.verPar=True
        self.paramFunc = self.getParams(tk.getSymbol())
        self.function = tk

    def finalizarVerificacaoParametros(self, err):
        if(self.paramNum != len(self.paramFunc)):
            tk = self.function
            err.addErr(tk.getSymbol(), tk, tk.getLinha(), 9)

        self.verPar= False
        self.paramFunc=None
        self.paramNum = 0
        self.function=None
        self.paramTk =None 
        self.paramEscopo=None

    def addParam(self, tk):
        if(self.verPar):
            self.paramTk = tk
            self.paramEscopo = self.peekEscopo()

    def verificarParametro(self,err):
        tk = self.paramTk
        paramEscopo = self.paramEscopo
        if(self.verPar):
            if(self.paramNum >= len(self.paramFunc)):
                err.addErr(tk.getSymbol(), tk, tk.getLinha(), 9)
            else:
                if(tk.getType()=='TNum'):
                    tipo1 = self.paramFunc[self.paramNum][2]
                    if(tipo1 != 'real' and tipo1 != 'int'):
                        err.addErr(tk.getSymbol(), tk, tk.getLinha(), 9)
                    self.paramNum = self.paramNum + 1
                else:
                    tipo = self.getTipo2(tk.getSymbol(), paramEscopo)
                    if(tipo != 'record'):
                        tipo1 = self.paramFunc[self.paramNum][2]
                        if(tipo != tipo1):
                            if(not(tipo=='int' and tipo1=='real')and not(tipo1=='int' and tipo=='real')):
                                err.addErr(tk.getSymbol(), tk, tk.getLinha(), 9)
                            self.paramNum = self.paramNum + 1
                        else:
                            self.paramNum = self.paramNum + 1