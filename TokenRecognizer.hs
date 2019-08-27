import Text.Regex.Posix

data TokenId = TNull 
             | TProgram        -- palavras reservadas
             | TBegin
             | TEnd
             | TConst
             | TType
             | TVar
             | TArray
             | TOf
             | TRecord
             | TFunction
             | TProcedure
             | TInteger
             | TReal
             | TWhile
             | TIf
             | TThen
             | TWrite
             | TRead
             | TElse
             | TRelacional     -- operadores e relacionais
             | TAtribuicao
             | TOperador
             | TVirgula        -- estruturais
             | TPontoEVirgula
             | TAbreColchetes
             | TFechaColchetes
             | TAbreParenteses
             | TFechaParenteses
             | TAspasDuplas       --valores
             | TVarDef
             | TAlfaNum
             | TNum
             | TAlfaNumId
             deriving (Show)



data Token a = Token TokenId String
             deriving (Show)


--let prog = ["program","funcoes",";","const","TAM","=","10",";","type","vetor","=","array","[","15","]","of","integer",";","aluno","=","record","nota1",",","nota2",":","real",";","end",";","var","A",",","B",",","C",",","D",":","integer",";","E",":","vetor",";","F",":","aluno",";"]

-- Aqui ele irá encontrar as regex. Irei alterar quando o Eduardo colocar a gramática no classroom

matchToken :: [Char] -> Token a
matchToken s
    | matchRegex s "program" = Token TProgram s
    | matchRegex s "begin" = Token TBegin s
    | matchRegex s "end" = Token TEnd s
    | matchRegex s "const" = Token TConst s
    | matchRegex s "type" = Token TType s
    | matchRegex s "var" = Token TVar s
    | matchRegex s "array" = Token TArray s
    | matchRegex s "of" = Token TOf s
    | matchRegex s "record" = Token TRecord s
    | matchRegex s "function" = Token TFunction s
    | matchRegex s "procedure" = Token TProcedure s
    | matchRegex s "integer" = Token TInteger s
    | matchRegex s "real" = Token TReal s
    | matchRegex s "while" = Token TWhile s
    | matchRegex s "if" = Token TIf s
    | matchRegex s "then" = Token TThen s
    | matchRegex s "write" = Token TWrite s
    | matchRegex s "read" = Token TRead s
    | matchRegex s "else" = Token TElse s
    -- operadores e relacionais
    | matchRegex s "[=><!]" = Token TRelacional s
    | matchRegex s ":=" = Token TAtribuicao s
    | matchRegex s "[+-/*]" = Token TOperador s
    -- estruturais
    | matchRegex s ";" = Token TPontoEVirgula s
    | matchRegex s "[,]" = Token TVirgula s
    | matchRegex s "[[]" = Token TAbreColchetes s
    | matchRegex s "[]]" = Token TFechaColchetes s  
    | matchRegex s "[(]" = Token TAbreParenteses s
    | matchRegex s ")" = Token TFechaParenteses s
    
    -- valores
    | matchRegex s "\"" = Token TAspasDuplas s
    | matchRegex s ":" = Token TVarDef s
    | matchRegex s "[:alpha:][:alnum:]*" = Token TAlfaNumId s
    | matchRegex s "[:alnum:]*" = Token TAlfaNum s
    -- falta verificar como funcionaria a verificação de se um alfanum inciado por char é string ou id
    | matchRegex s "^[0-9]+$" = Token TNum s
    | matchRegex s "^[0-9]+.[0-9]+$" = Token TNum s

    | otherwise = Token TNull ""


matchRegex :: [Char] -> [Char] -> Bool
matchRegex s p = s =~ p

