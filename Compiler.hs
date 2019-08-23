import System.IO

main =
    readFile "program" >>= -- substituir a string pelo caminho do programa
    putStr -- substituir aqui pela chamada da função que irá separar os tokens