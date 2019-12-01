#Funcoes para geração de codigo interemdiario
from sintatico import TokenTree
from token import Token
from follow import *

#Ainda não sei se é o melhor jeito, mas essa classe teria os 4 valores de uma instrução
# de codigo intermediario, daí a gente ia adicionado de uma em uma instrução, sla
class Instrucao():
    def __init__(self, comando):
        self.instrucao = [comando]
        self.qtdTemporarios = 0

    def addEndereco(self, endereco):
        if(len(self.instrucao < 4)):
            self.instrucao.append(endereco)

    def incrementarTemporarios(self):
        self.qtdTemporarios = self.qtdTemporarios + 1

    def getTempo(self):
        return self.qtdTemporarios

# Aqui é a função que seria chamada pela main, vai iniciar um vetor vazio
#de instruções que vai ser retornado, esse vetor será nosso programa final
def gerarCodigoIntermediario(tree):
    instrucoes = []
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
    print('Constantes')
    command = tree.children
    # Aqui deverá chamar uma função para constvalor que irá gerar uma instrução do 
    # tipo Mov t1 [valor da exp mat]. Quando a gente chamar a função pra gerar a instrução
    # de constValor, ela possivelmente vai gerar varias instruções e varios registradores
    # temporarios. A cada instrução que vai atribuir um valor a um registrador temporario,
    # a gente teria que incrementar a quantidade de temporarios.
    print('Mov ' + str(command[0].getRoot().getSymbol()) + ' value')  # substituir para pegar o valor do registrador temporario atual
    if(len(command) > 4): #Se o tamanho dos filhos for maior que 4, significa que tem a instrução constantes2
        matchConstantes2(command[4], inst)

# A função pra tratar constantes2 precisa ser diferente pq constantes2 só lê um id e uma atribuição
# e então chama constantes3. A gente pode ler constantes3 direto daqui pra achar o valor.
def matchConstantes2(tree, inst):
    command = tree.children
    var = command[0].getRoot().getSymbol()
    # Aqui deverá chamar uma função para constvalor que irá gerar uma instrução do tipo Mov t1 [valor da exp mat]
    val = 'value' # substituir para pegar o valor do registrador temporario atual
    print('Mov ' + str(var) + ' ' + str(val))
    if(len(command[1].children) > 3): #Verifica se existe constantes2 dentro de constantes3
        matchConstantes2(command[1].children[3], inst)


def matchRotinas(tree, inst):
    # Vai definir o label pra função
    print('rotinas')
    for child in tree.children:
        matchNode(child, inst)
    return

def matchComandos(tree, inst):
    # Um caso para atribuição (terá que verificar se o lado direito é função, array, etc)
    # Um caso para while
    # Um caso para if (e verificar se existirá um else)
    # Um caso para write
    # Um caso para read
    print('comandos')
    for child in tree.children:
        matchNode(child, inst)
    return

#Criar funções também para tratar exp_mat, exp logica, 