import Text.Regex.Posix

data TokenId = TknConditional
             | TknLoop
             | TknNumber
             | TknString
             | TknIdentifier
             | TknRelacional
             | TknPontoVirgula
             deriving (Show)

data Token a = Token TokenId String
             deriving (Show)

-- Aqui ele irá encontrar as regex. Irei alterar quando o Eduardo colocar a gramática no classroom
matchToken :: String -> Token a
matchToken s
    | matchRegex s "if" = Token TknConditional s
    | matchRegex s "while" = Token TknLoop s 
    | matchRegex s ";" = Token TknPontoVirgula s
    | matchRegex s "==" = Token TknRelacional s
    | matchRegex s "^[0-9]+$" = Token TknNumber s
    | matchRegex s "^[0-9]+.[0-9]+$" = Token TknNumber s
    | matchRegex s "^\"[^\"]*\"$" = Token TknString s --Verificar como fazer o regex para strings
    | otherwise = Token TknIdentifier s

matchRegex :: String -> String -> Bool
matchRegex s p = s =~ p