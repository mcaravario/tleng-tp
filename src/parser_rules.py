from tokens import *
from expression import *

precedence = (
    ('left', 'LEQ', 'GEQ', 'LT', 'GT'),
    ('left', 'EQUAL', 'LNOTEQ'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MULT', 'DIV'),
    ('left', 'MOD', 'POW'),
    ('left', 'AND', 'OR')
)

type_by_id = {}
register_types = {}


def tab(s):
    return "".join(["\t" + v for v in s.splitlines(True)])


def lineerr(n):
    return "Error de parseo en línea {}: ".format(n)


def p_error(se):
    if se is None:
        msg = "Parsing error."
    else:
        msg = lineerr(se.lineno)
        msg += "\n\trule: " + se.type
        msg += "\n\tsubexpression value: " + se.value
        msg += "\n\tlineno: " + str(se.lineno)
    raise Exception(msg)


# INSTR

def p_instrlsit(se):
    """
    instrlist : instr
              | instr instrlist
    """
    if len(se) == 2: # instr
        se[0] = se[1]
    else:
        se[0] = Instruccion(se[1].texto + se[2].texto)

def p_instr(se):
    """
    instr : COMMENT
          | assign SEMICOLON
          | call SEMICOLON
          | conditional
          | loop
    """
    if len(se) == 2 and (type(se[1]) is str): # COMMENT
        se[0] = Instruccion(se[1] + "\n")
    elif len(se) == 2 and (type(se[1]) is Instruccion): # conditional | loop
        se[0] = Instruccion(se[1].texto)
    else: # assign SEMICOLON | call SEMICOLON
        se[0] = Instruccion(se[1].texto + ";\n")

def p_block(se):
    """
    block : instr
          | LBRACE instrlist RBRACE
    """
    if len(se) == 2: # instr
        se[0] = Instruccion("\n" + tab(se[1].texto))
    else: # LBRACE instrlist RBRACE
        se[0] = Instruccion(" {\n" + tab(se[2].texto) + "}\n")


# CONDITIONALS

def p_conditional(se):
    """
    conditional : IF LPARENT term RPARENT block elsebranch
    """
    if se[6].texto == "": # IF LPARENT term RPARENT block
        se[0] = Instruccion("if ({}){}".format(se[3].texto, se[5].texto))
    else: # IF LPARENT term RPARENT block ELSE block
        # esto no puede generar una excepción IndexError, pues los terminos son
        # no vacios y los bloques siempre terminan en '\n'
        if se[5].texto[-2] == "}":
            se[0] = Instruccion("if ({}){} {}".format(se[3].texto, se[5].texto.rstrip(), se[6].texto))
        else:
            se[0] = Instruccion("if ({}){}{}".format(se[3].texto, se[5].texto, se[6].texto))

def p_elsebranch(se):
    """
    elsebranch :
               | ELSE block
    """
    if len(se) == 1: #
        se[0] = Instruccion("")
    elif len(se) == 3: # ELSE ifblock
        se[0] = Instruccion("else {}".format(se[2].texto))


# LOOP

def p_loop(se):
    """
    loop : FOR LPARENT assign SEMICOLON term SEMICOLON term RPARENT block
         | WHILE LPARENT term RPARENT block
         | DO block WHILE LPARENT term RPARENT SEMICOLON
    """
    if len(se) == 10: # FOR LPARENT assign SEMICOLON term SEMICOLON term RPARENT block
        se[0] = Instruccion("for ({}; {}; {}){}".format(se[3].texto,
                                                        se[5].texto,
                                                        se[7].texto,
                                                        se[9].texto))
    elif len(se) == 6: # WHILE LPARENT term RPARENT block
        se[0] = Instruccion("while ({}) {}".format(se[3].texto, se[5].texto))
    else: # DO block WHILE LPARENT term RPARENT SEMICOLON
        # esto no puede generar una excepción IndexError, pues los terminos son
        # no vacios y los bloques siempre terminan en '\n'
        if se[2].texto[-2] == "}":
            se[0] = Instruccion("do {} while ({});\n".format(se[2].texto.rstrip(), se[5].texto))
        else:
            se[0] = Instruccion("do {}while ({});\n".format(se[2].texto, se[5].texto))


# ASSIGN

def p_assign(se):
    "assign : ID ASSIGN term"
    se[0] = Instruccion(se[1] + " = " + se[3].texto)
    type_by_id[se[1]] = se[3].tipo
    if(se[3].tipo == 'REGISTER'):
        register_types[se[1]] = se[3].tiposreg


# CALL

def p_call(se):
    """
    call : MULTESCALAR LPARENT termlist RPARENT
         | CAPITALIZAR LPARENT termlist RPARENT
         | COLINEALES LPARENT termlist RPARENT
         | PRINT LPARENT termlist RPARENT
         | LENGTH LPARENT termlist RPARENT
    """
    msg = lineerr(se.lineno(1)) + se[1] + ": "
    if se[1] == "multiplicacionEscalar":
        if len(se[3]) != 2 and len(se[3]) != 3:
            raise Exception(msg + "se esparaban 2 o 3 parámetros")
        if se[3][0].tipo != "ARR_NUMBER":
            raise Exception(msg + "se esperaba un arreglo numérico")
        if se[3][1].tipo != "NUMBER":
            raise Exception(msg + "se esparaba un escalar")
        if len(se[3]) == 3 and se[3][2].tipo != "BOOL":
            raise Exception(msg + "se esperaba un booleano")
    elif se[1] == "capitalizar":
        if len(se[3]) != 1:
            raise Exception(msg + "se esperaba un parámetro")
        if se[3][0].tipo != "STRING":
            raise Exception(msg + "se esperaba una cadena")
    elif se[1] == "colineales":
        if len(se[3]) != 2:
            raise Exception(msg + "se esperaban 2 parámetros")
        if se[3][0].tipo != "ARR_NUMBER" or se[3][1].tipo != "ARR_NUMBER":
            raise Exception(msg + "se esperaban arreglos numéricos")
    elif se[1] == "print":
        if len(se[3]) != 1:
            raise Exception(msg + "se esperaba un parámetro")
    elif se[1] == "length":
        if len(se[3]) != 1:
            raise Exception(msg + "se esperaba un parámetro")
        if se[3][0].tipo != "STRING" and not se[3][0].tipo.startswith("ARR_"):
            raise Exception(msg + "se esperaba una cadena o un arreglo")
    else:
        raise Exception(msg + "función desconocida")
    se[0] = Instruccion("{}({})".format(se[1], ", ".join(t.texto for t in se[3])))


# ARI

# def p_ari_add(se):
#     "ari_a : ari_a ADD ari_t"
#     if se[1].tipo != se[3].tipo:
#         raise Exception("NO ESTAN BIEN LOS TIPOS")
#     se[0] = Termino(se[1].texto + " + " + se[3].texto, "INT")

# def p_ari_a2t(se):
#     "ari_a : ari_t"
#     se[0] = se[1]

# def p_ari_mult(se):
#     "ari_t : ari_t MULT ari_f"
#     se[0] = Termino(se[1].texto + " * " + se[3].texto, "INT")

# def p_ari_t2f(se):
#     "ari_t : ari_f"
#     se[0] = se[1]

# def p_ari_f2term(se):
#     "ari_f : term"
#     se[0] = se[1]

# def p_ari_parens(se):
#     "ari_f : LPARENT ari_a RPARENT"
#     se[0] = Termino("(" + se[2].texto + ")", "INT")


# TERM

def p_term(se):
    """
    term : ID
         | RES
         | literal
         | array
         | arraymember
         | register
         | registermember
         | unaryop
         | binaryop
         | LPARENT term RPARENT
         | term QUESTION term COLON term
    """
    if len(se) == 4: # LPARENT term RPARENT
        se[0] = Termino("({})".format(se[2].texto), se[2].tipo)
    elif len(se) == 6: # term QUESTION term COLON term
        msg = lineerr(se.lineno(2))
        if se[1].tipo != "BOOL":
            msg += "se esperaba una expresión booleana"
            raise Exception(msg)
        elif se[3].tipo != se[5].tipo:
            msg += "las ramas del operador ?: deben tener el mismo tipo"
            raise Exception(msg)
        se[0] = Termino("{} ? {} : {}".format(se[1].texto, se[3].texto, se[5].texto), se[3].tipo)
    elif type(se[1]) is Termino: # literal | unaryop | binaryop | register
                                 # | registermember| array | arraymember
        se[0] = se[1]
    else: # ID | RES
        se[0] = Termino(se[1], "UNKNOWN")

def p_literal(se):
    """
    literal : NUMBER
            | STRING
            | FALSE
            | TRUE
    """
    se[0] = Termino(se[1][0], se[1][1])

def p_termlist(se):
    """
    termlist :
             | term
             | term COMMA termlist
    """
    if len(se) == 1: #
        se[0] = []
    elif len(se) == 2: # term
        se[0] = [se[1]]
    elif len(se) == 4: # term COMMA termlist
        se[0] = [se[1]] + se[3]


# ARRAY

def p_array(se):
    """
    array : LBRACKET termlist RBRACKET
    """
    if len(se[2]) == 0: # LBRACKET RBRACKET
        tipo = "UNKNOWN"
    else: # LBRACKET termlist RBRACKET
        tipo = se[2][0].tipo
        if any(e.tipo != tipo for e in se[2]):
            msg = lineerr(se.lineno(1))
            msg += " los elementos del arreglo no son del mismo tipo."
            raise Exception(msg)
    se[0] = Termino("[" + ", ".join(e.texto for e in se[2]) + "]", "ARR_" + tipo)

def p_arraymember(se):
    """
    arraymember : ID LBRACKET term RBRACKET
    """
    if se[2].tipo != "NUMBER":
        msg = lineerr(se.lineno(1))
        msg += " el índice del arreglo no es numérico."
        raise Exception(msg)
    # TODO: determinar tipo en base al ID sobre el que se usa
    se[0] = Termino("{}[{}]".format(se[1], se[3].texto), "UNKNOWN")


# REGISTER

def p_register(se):
    """
    register : LBRACE registerlist RBRACE
    """
    tiposreg = {}
    for e in se[2]:
        tiposreg[e[0]] = e[2]
    se[0] = Termino("{ " + ", ".join(e[1] for e in se[2]) + " }", "REGISTER", tiposreg)

def p_registerlist(se): # TODO: sacar el shift-reduce?
    """
    registerlist :
                 | ID COLON term
                 | ID COLON term COMMA registerlist
    """
    if len(se) == 1: #
        se[0] = []
    elif len(se) == 4: # ID COLON term
        se[0] = [(se[1], "{}: {}".format(se[1], se[3].texto), se[3].tipo)]
    else: # ID COLON term COMMA registerlist
        se[0] = [(se[1], "{}: {}".format(se[1], se[3].texto), se[3].tipo)] + se[5]

def p_registermember(se):
    """
    registermember : ID DOT ID
    """
    # TODO: determinar tipo en base al ID sobre el que se usa y el ID con el
    # cual se accede
    reg = register_types.get(se[1])
    if reg is None:
        tipo = "UNKOWN"
    else:
        tipo = reg.get(se[3],"UNKOWN")
    se[0] = Termino("{}.{}".format(se[1], se[3]), tipo)


# UNARYOP

def p_unaryop(se): # TODO: hacer algo
    """
    unaryop : term
    """
    # quizas unaryop : op term


# BINARYOP

def p_binaryop(se): # TODO: hacer algo
    """
    binaryop : term ADD term
             | term SUB term
             | term MULT term
             | term DIV term
             | term MOD term
             | term POW term
             | term AND term
             | term OR term
             | term LT term
             | term LEQ term
             | term GT term
             | term GEQ term
             | term EQUAL term
             | term LNOTEQ term
    """
    type_res = 'UNKNOWN'
    if se[2] == '+':
        if se[1].tipo == 'NUMBER' and se[3].tipo == 'NUMBER':
            type_res = 'NUMBER'
        elif se[1].tipo == 'STRING' and se[3].tipo == 'STRING':
            type_res = 'STRING'
    elif se[2] == '-' or se[2] == '*' or se[2] == '/' or se[2] == '%' or se[2] == '^':
        if se[1].tipo == 'NUMBER' and se[3].tipo == 'NUMBER':
            type_res = 'NUMBER'
    elif se[2] == 'AND' or se[2] == 'OR':
        if se[1].tipo == 'BOOL' and se[3].tipo == 'BOOL':
            type_res = 'BOOL'
    else:
        if se[1].tipo == se[3].tipo:
            type_res = se[1].tipo

    if type_res == 'UNKNOWN':
        msg = lineerr(se.lineno(2))
        msg += " tipos incompatibles para " + se[2]
        raise Exception(msg)

    se[0] = Termino("{} {} {}".format(se[1].texto, se[2], se[3].texto), type_res)
