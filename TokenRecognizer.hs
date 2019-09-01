import Text.Regex.Posix
import Tokens

--let prog = ["program","funcoes",";","const","TAM","=","10",";","type","vetor","=","array","[","15","]","of","integer",";","aluno","=","record","nota1",",","nota2",":","real",";","end",";","var","A",",","B",",","C",",","D",":","integer",";","E",":","vetor",";","F",":","aluno",";"]

matchToken :: [Char] -> Token
matchToken s
    | matchRegex s "^program$" = Token TProgram s
    | matchRegex s "^begin$" = Token TBegin s
    | matchRegex s "^end$" = Token TEnd s
    | matchRegex s "^const$" = Token TConst s
    | matchRegex s "^type$" = Token TType s
    | matchRegex s "^var$" = Token TVar s
    | matchRegex s "^array$" = Token TArray s
    | matchRegex s "^of$" = Token TOf s
    | matchRegex s "^record$" = Token TRecord s
    | matchRegex s "^function$" = Token TFunction s
    | matchRegex s "^procedure$" = Token TProcedure s
    | matchRegex s "^integer$" = Token TInteger s
    | matchRegex s "^real$" = Token TReal s
    | matchRegex s "^while$" = Token TWhile s
    | matchRegex s "^if$" = Token TIf s
    | matchRegex s "^then$" = Token TThen s
    | matchRegex s "^write$" = Token TWrite s
    | matchRegex s "^read$" = Token TRead s
    | matchRegex s "^else$" = Token TElse s
    -- operadores e relacionais
    | matchRegex s "^[=><!]$" = Token TRelacional s
    | matchRegex s "^:=$" = Token TAtribuicao s
    | matchRegex s "^[+-/*]$" = Token TOperador s
    -- estruturais
    | matchRegex s "^;$" = Token TPontoEVirgula s
    | matchRegex s "^[,]$" = Token TVirgula s
    | matchRegex s "^[[]$" = Token TAbreColchetes s
    | matchRegex s "^[]]$" = Token TFechaColchetes s  
    | matchRegex s "^[(]$" = Token TAbreParenteses s
    | matchRegex s "^)$" = Token TFechaParenteses s
    | matchRegex s "^[.]$" = Token TPonto s
    -- valores
    | matchRegex s "^\"[a-zA-Z0-9]*\"$" = Token TString s
    | matchRegex s "^:$" = Token TVarDef s
    | matchRegex s "^[a-zA-Z_][:alnum:]*" = Token TId s
    | matchRegex s "^[0-9]+$" = Token TNum s
    | matchRegex s "^[0-9]+.[0-9]+$" = Token TNum s

    | otherwise = error "Erro lexico: no pattern found"

matchRegex :: [Char] -> [Char] -> Bool
matchRegex s p = s =~ p

