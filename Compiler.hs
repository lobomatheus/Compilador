import System.IO
import System.Environment
import TokenRecognizer

-- Para executar, chame:
-- runghc Compiler.hs "[nome do arquivo do programa]"
-- a variável inf armazena uma string contendo o programa inteiro

main = do
    args <- getArgs
    inf <- readFile (head args)
    putStr map (\x -> matchToken x) inf -- substituir aqui pela chamada da função que irá separar os tokens