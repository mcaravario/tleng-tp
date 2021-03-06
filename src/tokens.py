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
    "AND" : "AND",
    "OR" : "OR",
    "NOT" : "NOT"
}

tokens = [
    'NUMBER',
    'ID',
    'SEMICOLON',
    'COLON',
    'INLCOMMENT',
    'COMMENT',
    'RBRACE',
    'LBRACE',
    'RBRACKET',
    'LBRACKET',
    'RPARENT',
    'LPARENT',
    'ADD',
    'DEC',
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
    'MOD',
    'LT',
    'LEQ',
    'GEQ',
    'GT',
    'LNOTEQ',  #!=
    'QUESTION',
    'DOT',
    'STRING',
    'COMMA'
] + list(reserved.values())

tipo_UNKNOWN  = -1
tipo_BASICO   = 1
tipo_ARREGLO  = 2
tipo_REGISTRO = 3
tipo_BOOL     = 4
tipo_NUMBER   = 5
tipo_STRING   = 6
