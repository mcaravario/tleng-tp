from tokens import *

def t_error(tok):
    msg = "Unknown token @ line {0} column {1}:".format(tok.lineno,
                                                        tok.lexpos + 1)
    msg += "\n\tvalue: " + str(tok.value)
    raise Exception(msg)

def t_NEWLINE(tok):
    r"\n+"
    tok.lexer.lineno += len(tok.value)

def t_NUMBER(tok):
    r"[0-9]+(\.[0-9]+)?"
    tok.value = tok.value
    return tok

def t_ID(tok):
    r"[a-zA-Z][a-zA-Z0-9_]*"
    tok.type = reserved.get(tok.value, "ID")
    return tok

t_ignore_WHITESPACES = r"[ \t]+"

t_COMMENT = r"\#.*"

t_STRING = r"\"[^\"]*\""

t_SEMICOLON = r";"

t_COLON = r":"

t_RBRACE = r"}"

t_LBRACE = r"{"

t_RBRACKET = r"\]"

t_LBRACKET = r"\["

t_RPARENT = r"\)"

t_LPARENT = r"\("

t_ADD = r"\+"

t_ADDEQ = r"\+="

t_INC = r"\+\+"

t_ASSIGN = r"="

t_EQUAL = r"=="

t_SUB = r"-"

t_SUBEQ = r"-="

t_MULT = r"\*"

t_MULTEQ = r"\*="

t_DIV = r"/"

t_DIVEQ = r"/="

t_POW = r"\^"

t_AND = r"AND"

t_OR = r"OR"

t_NOT = r"NOT"

t_MOD = r"%"

t_LT = r"<"

t_LEQ = r"<="

t_GEQ = r">="

t_GT = r">"

t_LNOT = r"!"

t_LNOTEQ = r"!="

t_QUESTION = r"\?"

t_DOT = r"\."

t_COMMA = r","
