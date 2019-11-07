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
        self.confere = False
    
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


    #---------------------------provavelmente nao sera necessario (regra 1 cobre)
    """ def verificarCampoRegistro(self, idReg, idCampo):
        regis = list(filter((lambda x: x[4] == idReg and x[0]==idCampo)))
        if(lem(regs) == 0):
            return True
        return False """


    
    #---------------------------
    def getTipo(self, id, escopo):
        for s in self.table:
            if(s[0] == id and s[3]==escopo):
                return self.tratarTiposDefinidos(s[2])
        for s in self.table:
            if(s[0] == id and s[3]=='global'):
                return self.tratarTiposDefinidos(s[2])
        func = list(filter((lambda x: x[0]==escopo), self.table))
        if(len(func) > 0):
            if(func[0][1] == 'function' or func[0][1] == 'procedure'):
                for s in func[0][4]:
                    if(s[0] == id):
                        return self.tratarTiposDefinidos(s[2])
            else:
                return self.tratarTiposDefinidos(func[0][0])
        return ''
    
    def tratarTiposDefinidos(self, tipo):
        tipos = list(filter((lambda x: (x[1]=='tipo' or x[1]=='array') and x[0]==tipo), self.table))
        if(len(tipos) > 0):
            return self.tratarTiposDefinidos(tipos[0][2])
        else:
            return tipo

    def iniciarVerTipos(self, id):
        self.idEsquerda = id
        self.escopoEsquerda = self.peekEscopo()

    def verificarTipos(self, tk, err):
        if(self.idEsquerda != None):
            id2 = tk.getSymbol()
            if(tk.getType()== 'TNum'):
                tipo1 = self.getTipo(self.idEsquerda, self.escopoEsquerda)
                if tipo1 != 'int' and tipo1 != 'real':
                    err.addErr(tk.getSymbol(), tk, tk.getLinha(), 10)
                self.idEsquerda = None
                self.escopoEsquerda = None
            else:
                tipo2 = self.getTipo(id2, self.peekEscopo())
                if(tipo2 != 'record'):
                    #print(tipo2 + ' - ' + self.peekEscopo() + ' : ' + self.idEsquerda)
                    tipo1 = self.getTipo(self.idEsquerda, self.escopoEsquerda)
                    if(tipo1 != tipo2):
                        if(not(tipo1=='int' and tipo2=='real')):
                            err.addErr(tk.getSymbol(), tk, tk.getLinha(), 10)
                    self.idEsquerda = None
                    self.escopoEsquerda = None


    def verificarRegistro(self, tk, err):
        id = tk.getSymbol()
        escopoAtual = self.peekEscopo()
        #print(escopoAtual)
        #print(self.getRecords(escopoAtual))
        reg = list(filter((lambda x: (x[3] == escopoAtual and x[0] in self.getElements('record', escopoAtual)) and x[0] == id), self.table))
        if(len(reg) == 0):
            reg = list(filter((lambda x: (x[3] == 'global' and x[0] in self.getElements('record', 'global')) and x[0] == id), self.table))
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
                    err.addErr(tk.getSymbol(), tk, tk.getLinha(), 7)
        
    def getElements(self, classe, escopo):
        rec = list(filter((lambda x: (self.getTipo(x[0],escopo)==classe and x[3]==escopo)), self.table))
        rec2 = []
        for r in rec:
            rec2.append(r[0])
        return rec2

    def verificarVetor(self, tk, err):
        id = tk.getSymbol()
        escopoAtual = self.peekEscopo()
        reg = list(filter((lambda x: (x[3] == escopoAtual and x[0] in self.getElements('array', escopoAtual)) and x[0] == id), self.table))
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
                    err.addErr(tk.getSymbol(), tk, tk.getLinha(), 5)
        

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
