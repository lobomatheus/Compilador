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
        self.escopo=[]
        self.arrayCount = 0
    
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
            else: self.table.append(new)

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
    def mesmoNome(self, id):
        escopoAtual = self.peekEscopo()
        if(len(list(filter((lambda x: x[0] == id and x[3] == escopoAtual), self.table))) > 0):
            return True
        else: return False

    def verificarFuncao(self, id):
        funcs = list(filter((lambda x: (x[1] == 'function' or x[1] == 'procedure') and x[0] == id), self.table))
        if(len(funcs) == 0):
            return True
        return False

    def verificarCampoRegistro(self, idReg, idCampo):
        regis = list(filter((lambda x: x[4] == idReg and x[0]==idCampo)))
        if(lem(regs) == 0):
            return True
        return False

    def getTipo(self, id):
        for s in self.table:
            if(s[0] == id and s[4]==self.escopo.peek()):
                return s[2]
        for s in self.table:
            if(s[0] == id and s[4]=='global'):
                return s[2]
        return ''

    def verificarTipos(self, id1, id2):
        tipo1 = self.getTipo(id1)
        tipo2 = self.getTipo(id2)
        if(tipo1 != tipo2):
            return True
        return False


                
