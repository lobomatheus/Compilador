#Funcoes para geração de codigo interemdiario
from sintatico import TokenTree
from token import Token
from follow import *

#Ainda não sei se é o melhor jeito, mas essa classe teria os 4 valores de uma instrução
# de codigo intermediario, daí a gente ia adicionado de uma em uma instrução, sla

totalLinhas = 0

class Instrucao():
    def __init__(self, comando):
        self.instrucao = [comando]
        self.label = None

    def addEndereco(self, endereco):
        self.instrucao.append(endereco)

    def addLabel(self, label):
        self.label = label

class ConjInstrucao():
    def __init__(self):
        self.conj = []
        self.qtdTemporarios = 0

    def addInstrucao(self, inst):
        global totalLinhas
        totalLinhas = totalLinhas + 1
        self.conj.append(inst)

    def addConjInstrucao(self, dummyInst):
        for c in dummyInst.conj:
            self.conj.append(c)

    def incrementarTemporarios(self):
        self.qtdTemporarios = self.qtdTemporarios + 1

    def setTemp(self, inst):
        self.qtdTemporarios = inst.qtdTemporarios

    def getTempo(self):
        return "temp" + str(self.qtdTemporarios)

# Aqui é a função que seria chamada pela main, vai iniciar um vetor vazio
#de instruções que vai ser retornado, esse vetor será nosso programa final
def gerarCodigoIntermediario(tree):
    instrucoes = ConjInstrucao()
    matchNode(tree, instrucoes)
    return instrucoes

# Aqui ele verifica no nó raiz as instruções "principais"
#pelo que eu percebi (e tem chance de eu estar errado), qualquer
#outra instrução que possa vir a se tornar codigo intermediario
#é "subinstrução" delas, nunca vai aparecer "no topo", então
#a gente poderia tratar internamente e assim diminui a quantidade
#de ifs nessa função principal.
def matchNode(tree, inst):
    if(not tree.hasChildren()):
        return
    tk = tree.getRoot()

    #Esses sao os nós "principais"
    if(tk.getTokenCode() == TCONSTANTES):
        matchConstantes(tree, inst)
    elif(tk.getTokenCode() == TDEFROTINAS):
        matchRotinas(tree, inst)
    elif(tk.getTokenCode() == TCOMANDOS or tk.getTokenCode() == TCOMANDOS3):
        matchComandos(tree, inst)
    else: #se não for nenhum deles, passa pro próximo (não sei se o certo é passar assim mesmo)
        for child in tree.children:
            matchNode(child, inst)

        
    


# Aqui ele vai verificar o caso das constantes. Foi o único caso que eu fiz
# e acho que, fora a parte de pegar o valor que ta sendo atribuido, ta funcionando
# certinho.
def matchConstantes(tree, inst):
    # Pra cada constante que achar, a gente faz um Mov na memoria
    command = tree.children
    # Aqui deverá chamar uma função para constvalor que irá gerar uma instrução do 
    # tipo Mov t1 [valor da exp mat]. Quando a gente chamar a função pra gerar a instrução
    # de constValor, ela possivelmente vai gerar varias instruções e varios registradores
    # temporarios. A cada instrução que vai atribuir um valor a um registrador temporario,
    # a gente teria que incrementar a quantidade de temporarios.
    val = getValor(command[2], inst) # substituir para pegar o valor do registrador temporario atual

    i = Instrucao('Mov')
    i.addEndereco(str(command[0].getRoot().getSymbol()))
    i.addEndereco(val)
    inst.addInstrucao(i)

    if(len(command) > 4): #Se o tamanho dos filhos for maior que 4, significa que tem a instrução constantes2
        matchConstantes2(command[4], inst)

# A função pra tratar constantes2 precisa ser diferente pq constantes2 só lê um id e uma atribuição
# e então chama constantes3. A gente pode ler constantes3 direto daqui pra achar o valor.
def matchConstantes2(tree, inst):
    command = tree.children
    var = command[0].getRoot().getSymbol()
    # Aqui deverá chamar uma função para constvalor que irá gerar uma instrução do tipo Mov t1 [valor da exp mat]
    #print(command[1].children[0].getRoot().getSymbol())
    val = getValor(command[1].children[1], inst) # substituir para pegar o valor do registrador temporario atual
    i = Instrucao('Mov')
    i.addEndereco(var)
    i.addEndereco(val)
    inst.addInstrucao(i)
    if(len(command[1].children) > 3): #Verifica se existe constantes2 dentro de constantes3
        matchConstantes2(command[1].children[3], inst)


def matchBloco(tree, inst, label='', bloco_normal=False):
    command = tree.children
    if(bloco_normal):
        bloco = tree
    else:
        if(command[0].getRoot().getTokenCode() == TVAR):
            bloco = command[2]
        else:
            bloco = command[0]
    if(bloco.children[0].getRoot().getTokenCode() == TBEGIN):
        matchComandos(bloco.children[1], inst, label)
    else:
        matchComandos(bloco.children[0], inst, label)


def matchRotinas(tree, inst):
    # Vai definir o label pra função
    command = tree.children

    label = command[1].children[0].getRoot().getSymbol()

    if(command[0].getRoot().getTokenCode() == TFUNCTION):
        bloco = command[4]

        matchBloco(bloco, inst, label)

        inst.addInstrucao(Instrucao('RTN'))

        if(len(command) == 6):
            matchRotinas(command[5], inst)
    else:
        bloco = command[2]

        matchBloco(bloco, inst, label)

        if(len(command) == 4):
            matchRotinas(command[3], inst)


    return

def matchComandos(tree, inst, label=''):
    #print(tree.getRoot().getSymbol() + str(tree.getRoot().getLinha()))
    tk = tree.children[0].getRoot()
    # Um caso para atribuição (terá que verificar se o lado direito é função, array, etc)
    if(tk.getTokenCode() == TID):
        
        if(tree.children[1].getRoot().getTokenCode() == TNOME2):
            val = pegarExpMat(tree.children[3].children, inst)#'value' # substituir para pegar o valor do registrador temporario atual
        else:
            val = pegarExpMat(tree.children[2].children, inst)
        i = Instrucao("Mov")
        id = tree.children[0].getRoot().getSymbol()
        if(tree.children[1].getRoot().getTokenCode() == TNOME2):
            i.addEndereco(id + getIdName(tree.children[1], inst))
        else:
            i.addEndereco(id)
        if(val == None):
            i.addEndereco(inst.getTempo())
        else:
            i.addEndereco(val)
        if(label!=''): i.addLabel(label)
        inst.addInstrucao(i)
    # Um caso para while
    if(tk.getTokenCode() == TWHILE):
        tratarWhile(tree, inst)
    
    # Um caso para if (e verificar se existirá um else)
    if(tk.getTokenCode() == TIF):
        tratarIfElse(tree, inst)

    
    # Um caso para write
    # Um caso para write
    if(tk.getTokenCode() == TWRITE):
        i = Instrucao("str")
        #val = tree.children[1].getRoot().getSymbol()
        var = getValor(tree.children[1], inst)
        i.addEndereco(var)
        if(label!=''): i.addLabel(label)
        #i.addEndereco(val)
        inst.addInstrucao(i)

    # Um caso para read
    if(tk.getTokenCode() == TREAD):
        i = Instrucao("lod")
        nome = tree.children[1]
        id = nome.children[0].getRoot().getSymbol()
        if(nome.children[1].getRoot().getTokenCode() == TNOME2):
            i.addEndereco(id + getIdName(nome.children[1], inst))
        else:
            i.addEndereco(id)
        if(label!=''): i.addLabel(label)
        inst.addInstrucao(i)

    tam = len(tree.children)
    if(tree.children[tam-1].getRoot().getTokenCode() == TCOMANDOS2):
        if(len(tree.children[tam-1].children) > 1):
            matchComandos(tree.children[tam-1].children[1], inst)
    
    #for child in tree.children:
    #    matchNode(child, inst)
    return

#Criar funções também para tratar exp_mat, exp logica, 

def getValor(tree, inst): #caso do const valor
    command = tree.children
    tk = tree.children[0].getRoot()

    if (tk.getTokenCode() == TSTRING):
        return tk.getSymbol()
    else:
        return pegarExpMat(command[0].children,inst)

def pegarExpMat(tree, inst):
    tk = tree[0].getRoot()

    if(tk.getTokenCode() == TNUM):
        t1 = tk.getSymbol()
        if(len(tree) > 1):
            op = tree[1].children[0].getRoot().getSymbol()
            if(op == '+'):
                i = Instrucao('Add')
            elif(op =='-'):
                i = Instrucao('Sub')
            elif(op == '*'):
                i = Instrucao('Mul')
            elif(op == '/'):
                i = Instrucao('Div')
            

            
            val = pegarExpMat(tree[1].children[1].children, inst)
            
            res = inst.getTempo()

            inst.incrementarTemporarios()
            i.addEndereco(inst.getTempo())

            
            if(val == None):
                i.addEndereco(res)
            else:
                i.addEndereco(val)
            i.addEndereco(t1)
            inst.addInstrucao(i)
        else:
            return t1

    elif(tk.getTokenCode() == TABREPARENTESES):  
        pegarExpMat(tree[0].children)
    elif(tk.getTokenCode() == TNOMENUM):
        id = tree[0].children[0].getRoot().getSymbol() # pega o id do nomenum
        if(len(tree[0].children) > 1): #se nomenum tem nome3
            command = tree[0].children[1].children # filhos de nome3
        
            if(command[0].getRoot().getTokenCode() == TABREPARENTESES): #se nome3 é abre parenteses
                i = Instrucao('Call')
                i.addEndereco(id)
                inst.addInstrucao(i)
                return 'Rtn'

            else: #se nao é abre parenteses, é nome2
                id = id + getIdName(command[0], inst) #adiciona o resto do nome ao valor    
        if(len(tree) > 1):
            op = tree[1].children[0].getRoot().getSymbol() #pega o operador
            if(op == '+'):
                i = Instrucao('Add')
            elif(op =='-'):
                i = Instrucao('Sub')
            elif(op == '*'):
                i = Instrucao('Mul')
            elif(op == '/'):
                i = Instrucao('Div')
            
            
            val = pegarExpMat(tree[1].children[1].children, inst)
            
            res = inst.getTempo()

            inst.incrementarTemporarios()
            i.addEndereco(inst.getTempo())
            if(val == None):
                i.addEndereco(res)
            else:
                i.addEndereco(val)
            i.addEndereco(id)
            inst.addInstrucao(i)
        else:
            #val = tree[0].children[0].getRoot().getSymbol()
            i = Instrucao('Mov')
            inst.incrementarTemporarios()
            i.addEndereco(inst.getTempo())
            i.addEndereco(id)
            inst.addInstrucao(i)

def tratarWhile(tree, inst):

    command = tree.children

    linhaRetorno = totalLinhas + 1

    condicao = tratarExpLogica(command[1], inst)

    jmp = Instrucao('Jnz')
    jmp.addEndereco(inst.getTempo())
    
    dummyInst = ConjInstrucao()
    dummyInst.setTemp(inst)

    if(not condicao):
        #jmp.addEndereco(len(inst.conj) + len(dummyInst.conj) + 2)
        matchBloco(command[2], dummyInst, bloco_normal=True)
        jmp.addEndereco(totalLinhas + 2)
        inst.addInstrucao(jmp)
    else:
        jmp.addEndereco(totalLinhas + 3)
        matchBloco(command[2], dummyInst, bloco_normal=True)
        jmp2 = Instrucao('Jmp')
        #jmp2.addEndereco(len(inst.conj) + len(dummyInst.conj) + 3)
        jmp2.addEndereco(totalLinhas + 4)
        inst.addInstrucao(jmp)
        inst.addInstrucao(jmp2)

    inst.addConjInstrucao(dummyInst)
    inst.setTemp(dummyInst)    

    jmp3 = Instrucao('Jmp')
    jmp3.addEndereco(str(linhaRetorno))
    inst.addInstrucao(jmp3)


def tratarIfElse(tree, inst):
    
    command = tree.children

    condicao = tratarExpLogica(command[1], inst) #verifica qual será o valor de retorno
    # Agora precisaremos saber:
    # - se tem else e para onde dar jump
    #print(condicao)
    if(condicao):
        #aqui, condicao != 0, ou seja, condicao tem que ser =1, então se condicao != 1, da jump
        # o jump será para quando acabar a instrução. Logo, tem que adicionar a linha para onde vai pular
        jmp = Instrucao('Jnz')
        jmp.addEndereco(inst.getTempo())
        jmp.addEndereco(totalLinhas + 4)
        inst.addInstrucao(jmp)

        if(len(command) > 4):
            if(command[4].getRoot().getTokenCode() == TELSE):
                elseCommand = command[4].children
                elseInst = ConjInstrucao()
                elseInst.setTemp(inst)
                matchBloco(elseCommand[1], elseInst, bloco_normal=True)
                inst.addConjInstrucao(elseInst)
                inst.setTemp(elseInst)

        jmp2 = Instrucao('Jmp')

        dummyInst = ConjInstrucao()
        dummyInst.setTemp(inst)
        matchBloco(command[3], dummyInst, bloco_normal=True)

        #jmp2.addEndereco(str(len(inst.conj) + len(dummyInst.conj) + 2))
        jmp2.addEndereco(totalLinhas + 2)
        inst.addInstrucao(jmp2)
        #print('jmp2')
        
        inst.setTemp(dummyInst)
        inst.addConjInstrucao(dummyInst)
    else:
        # se condicao = 0, satisfaz, então é só pular o bloco if se nao for

        jmp = Instrucao('Jnz')
        jmp.addEndereco(inst.getTempo())

        

        dummyInst = ConjInstrucao()
        dummyInst.setTemp(inst)
        matchBloco(command[3], dummyInst, bloco_normal=True)

        #jmp.addEndereco(str(len(inst.conj) + len(dummyInst.conj) + 1))
        jmp.addEndereco(totalLinhas + 3)
        inst.addInstrucao(jmp)
        
        inst.setTemp(dummyInst)
        inst.addConjInstrucao(dummyInst)

        if(len(command) > 4):
            if(command[4].getRoot().getTokenCode() == TELSE):
                

                elseCommand = command[4].children
                elseInst = ConjInstrucao()
                elseInst.setTemp(inst)
                matchBloco(elseCommand[1], elseInst, bloco_normal=True)
                
                jmp2 = Instrucao('Jmp')
                #jmp2.addEndereco(len(inst.conj) + len(elseInst.conj) + 2)
                jmp2.addEndereco(totalLinhas + 2)
                inst.addInstrucao(jmp2)

                inst.addConjInstrucao(elseInst)
                inst.setTemp(elseInst)


def tratarExpLogica(tree, inst):
    ''' 
    operações possiveis:
    x = y: eql e verifica se temp = 1
    x < y: les e verifica se temp = 1
    x > y: les e verifica se temp = 0
    x ! y: eql e verifica se temp = 0

    exp logica:
        1- verifica primeiro valor
        2- verifica o operador logico e faz como está acima com um temporario que será gerado
        3- verifica o valor da proxima exp logica (vai retornar um temporario)
        4- repete o processo recursivamente até terminarem as exp logicas
        5- salva todo o codigo

        obs: não tem "and", "not" nem "or", o que facilita muito as coisas
        problema: é possível fazer, por exemplo: x = y < x > z = a < 0, não deveria ser possível
        esse problema faclita bastante o trabalho
    '''

    command = tree.children

    val1 = pegarExpMat(command[0].children, inst) #aqui pegaremos o registrador temporario
    if(val1 == None):
        temp1 = inst.getTempo()
    else:
        temp1 = val1

    if(len(command) > 1):
        val2 = tratarExpLogica(command[1].children[1] ,inst)
        if(val2 == None):
            temp2 = inst.getTempo()
        else:
            temp2 = val2

        opLogico = command[1].children[0]
        if(opLogico.getRoot().getSymbol() == '='):
            i = Instrucao('Eql')
            inst.incrementarTemporarios()
            i.addEndereco(inst.getTempo())
            i.addEndereco(temp1)
            i.addEndereco(temp2)
            inst.addInstrucao(i)
            return 1

        elif(opLogico.getRoot().getSymbol() == '!'):
            i = Instrucao('Eql')
            inst.incrementarTemporarios()
            i.addEndereco(inst.getTempo())
            i.addEndereco(temp1)
            i.addEndereco(temp2)
            inst.addInstrucao(i)
            return 0

        elif(opLogico.getRoot().getSymbol() == '<'):
            i = Instrucao('Les')
            inst.incrementarTemporarios()
            i.addEndereco(inst.getTempo())
            i.addEndereco(temp1)
            i.addEndereco(temp2)
            inst.addInstrucao(i)
            return 1
        
        elif(opLogico.getRoot().getSymbol() == '>'):
            i = Instrucao('Les')
            inst.incrementarTemporarios()
            i.addEndereco(inst.getTempo())
            i.addEndereco(temp1)
            i.addEndereco(temp2)
            inst.addInstrucao(i)
            return 0

    else:
        return val1


def tratarNomeNum(tree, inst):
    tk = tree.children[0].getRoot().getTokenCode()
    id = tree.children[0].getRoot().getSymbol() # pega o id do nomenum
    if(tk == TNUM):
        return id
    if(len(tree.children) > 1): #se nomenum tem nome3
        command = tree.children[1].children # filhos de nome3
    
        if(command[0].getRoot().getTokenCode() == TABREPARENTESES): #se nome3 é abre parenteses
            i = Instrucao('Call')
            i.addEndereco(id)
            i2 = Instrucao('Mov')
            inst.incrementarTemporarios()
            i2.addEndereco(inst.getTempo())
            i2.addEndereco('Rtn')
            inst.addInstrucao(i)
            inst.addInstrucao(i2)
        else: #se nao é abre parenteses, é nome2
            id = id + getIdName(command[0], inst) #adiciona o resto do nome ao valor    
    
    val = tree.children[0].getRoot().getSymbol()
    i = Instrucao('Mov')
    inst.incrementarTemporarios()
    i.addEndereco(inst.getTempo())
    i.addEndereco(val)
    inst.addInstrucao(i)

def getIdName(tree, inst):
    
    command = tree.children
    if(tree.getRoot().getTokenCode() == TID): #ID
        return tree.children[0].getRoot().getSymbol()

    if(command[0].getRoot().getTokenCode() == TPONTO): #Record
        nome = tree.children[1]
        id = nome.children[0].getRoot().getSymbol()
        if(len(nome.children) > 1 and nome.children[1].getRoot().getTokenCode() == TNOME2):
            return '.' + id + getIdName(nome.children[1], inst)
        else:
            return '.' + id 

    elif(command[0].getRoot().getTokenCode() == TABRECOLCHETES): #Vetor
        val = tratarNomeNum(command[1], inst)#Pega o valor do nome_num aqui
        if(val == None): val = inst.getTempo()
        return '[' + str(val) + ']'
