reserved = {
    "for": "FOR",
    "if": "IF",
    "else": "ELSE",
    "do": "DO",
    "while": "WHILE",
    "multiplicacionEscalar": "MULTESCALAR",
    "capitalizar": "CAPITALIZAR",
    "colineales": "COLINEALES",
    "print": "PRINT",
    "length": "LENGTH",
    "res": "RES",
    "begin": "BEGIN",
    "end": "END",
    "return": "RETURN",
    "true": "TRUE",
    "false": "FALSE",
}

tokens = [
    'NUMBER',
    'ID',
    'FOR',
    'SEMICOLON',
    'COMMENT',
    'RBRACE',
    'LBRACE',
    'IF',
    'RBRACKET',
    'LBRACKET',
    'RPARENT',
    'LPARENT',
    'ELSE',
    'DO',
    'WHILE',
    'MULTESCALAR',
    'CAPITALIZAR',
    'COLINEALES',
    'PRINT',
    'LENGTH',
    'ADD',
    'ADDEQ',
    'INC',
    'ASSIGN',
    'EQUAL',
    'SUB',
    'SUBEQ',
    'MULT',
    'MULTEQ',
    'DIV',
    'DIVEQ',
    'POW',
    'AND',
    'OR',
    'NOT',
    'MOD',
    'LT',
    'LEQ',
    'GEQ',
    'GT',
    'LNOT', #!
    'LNOTEQ',  #!=
    'TERNQUESTION',
    'TERNCOLON',
    'DOT',
    'STRING',
    'RES',
    'BEGIN',
    'END',
    'RETURN',
    'TRUE',
    'FALSE',
    'COMMA',
    'WHITESPACES',
    'NEWLINE'
] + list(reserved.values())
