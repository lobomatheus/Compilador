import System.IO
import System.Environment

-- Para executar, chame:
-- runghc Compiler.hs "[nome do arquivo do programa]"
-- a variável inf armazena uma string contendo o programa inteiro

main = do
    args <- getArgs
    inf <- readFile (head args)
    putStr inf -- substituir aqui pela chamada da função que irá separar os tokens