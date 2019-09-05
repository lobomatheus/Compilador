import System.IO
import System.Environment
--import TokenRecognizer
import TreeTest.hs

-- Para executar, chame:
-- runghc Compiler.hs "[nome do arquivo do programa]"
-- a variável inf armazena uma string contendo o programa inteiro

main = do
    args <- getArgs
    --inf <- readFile (head args)
    --putStr map (\x -> matchToken x) inf -- substituir aqui pela chamada da função que irá separar os tokens
    inh <- openFile (head args) ReadMode
    --testeFunc inh
    initial inh

{-
testeFunc :: Handle -> IO()
testeFunc inh = 
    do ineof <- hIsEOF inh
       if ineof
        then return ()
        else do
            n1 <- func1 inh
            n2 <- func2 inh
            putChar n1
            putChar n2
            n3 <- (hGetChar inh)
            putChar n3
            testeFunc inh

func1 :: Handle -> IO Char
func1 inh = (hGetChar inh)

func2 :: Handle -> IO Char
func2 inh = (hGetChar inh)
-}