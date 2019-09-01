module Tokens(
    TokenId(..),
    Token(..)
) where

data TokenId = TNull           -- TOKENS TERMINAIS
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
             | TPonto
             | TString        --valores
             | TVarDef
             | TId
             | TNum
             deriving (Show)

data TokenNT = TPrograma
             | TCorpo
             | TDeclar
             | TDefConst
             | TDefTipos
             | TDefVar
             | TConstantes
             | TConstante
             | TTipos
             | TTipo
             | TVariaveis
             | TVariavel
             | TListaId
             | TTipoDado
             | TDefRotinas
             | TFuncao
             | TProcedimento
             | TNomeRotina
             | TBlocoRotina
             | TBloco
             | TComandos
             | TComando
             | TBlocoElse
             | TValor
             | TParametros
             | TParametro
             | TListaParam
             | TExpLogica
             | TExpMatematica
             | TNomeNumero
             | TNome
            deriving (Show)

data Token = Token TokenId String
           | TknNT TokenNT
             deriving (Show)