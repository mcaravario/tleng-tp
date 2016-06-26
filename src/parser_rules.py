from tokens import *
from expression import *


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
    conditional : IF LPARENT expression RPARENT block elsebranch
    """
    if se[6].texto == "": # IF LPARENT expression RPARENT block
        se[0] = Instruccion("if ({}){}".format(se[3].texto, se[5].texto))
    else: # IF LPARENT expression RPARENT block ELSE block
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
    loop : FOR LPARENT assign SEMICOLON expression SEMICOLON expression RPARENT block
         | WHILE LPARENT expression RPARENT block
         | DO block WHILE LPARENT expression RPARENT SEMICOLON
    """
    if len(se) == 10: # FOR LPARENT assign SEMICOLON expression SEMICOLON expression RPARENT block
        se[0] = Instruccion("for ({}; {}; {}){}".format(se[3].texto,
                                                        se[5].texto,
                                                        se[7].texto,
                                                        se[9].texto))
    elif len(se) == 6: # WHILE LPARENT expression RPARENT block
        se[0] = Instruccion("while ({}) {}".format(se[3].texto, se[5].texto))
    else: # DO block WHILE LPARENT expression RPARENT SEMICOLON
        # esto no puede generar una excepción IndexError, pues los terminos son
        # no vacios y los bloques siempre terminan en '\n'
        if se[2].texto[-2] == "}":
            se[0] = Instruccion("do {} while ({});\n".format(se[2].texto.rstrip(), se[5].texto))
        else:
            se[0] = Instruccion("do {}while ({});\n".format(se[2].texto, se[5].texto))


# ASSIGN
# TODO: +=, -=, *=, /=

def p_assign(se):
    "assign : ID ASSIGN expression"
    se[0] = Instruccion(se[1] + " = " + se[3].texto)
    type_by_id[se[1]] = se[3].tipo
    if(se[3].tipo == 'REGISTER'):
        register_types[se[1]] = se[3].tiposreg


# CALL

def p_call(se):
    """
    call : MULTESCALAR LPARENT expressionlist RPARENT
         | CAPITALIZAR LPARENT expressionlist RPARENT
         | COLINEALES LPARENT expressionlist RPARENT
         | PRINT LPARENT expressionlist RPARENT
         | LENGTH LPARENT expressionlist RPARENT
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


# TERM

def p_expression(se):
    """
    expression : ID
               | RES
               | literal
               | array
               | arraymember
               | register
               | registermember
               | unaryop
               | binaryop
               | expression QUESTION expression COLON expression
    """
    if len(se) == 6: # expression QUESTION expression COLON expression
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
        msg = "{}{}: ".format(lineerr(se.lineno(1)), se[1])
        if se[1] not in type_by_id:
            raise Exception(msg + "variable no declarada")
        se[0] = Termino(se[1], type_by_id[se[1]], register_types.get(se[1]))

def p_literal(se):
    """
    literal : NUMBER
            | STRING
            | FALSE
            | TRUE
    """
    se[0] = Termino(se[1][0], se[1][1])

def p_expressionlist(se):
    """
    expressionlist :
                   | expression
                   | expression COMMA expressionlist
    """
    if len(se) == 2: # expression
        se[0] = [se[1]]
    elif len(se) == 4: # expression COMMA expressionlist
        se[0] = [se[1]] + se[3]


# ARRAY

def p_array(se):
    """
    array : LBRACKET expressionlist RBRACKET
    """
    if len(se[2]) == 0: # LBRACKET RBRACKET
        tipo = "UNKNOWN"
    else: # LBRACKET expressionlist RBRACKET
        tipo = se[2][0].tipo
        if any(e.tipo != tipo for e in se[2]):
            msg = lineerr(se.lineno(1))
            msg += "los elementos del arreglo no son del mismo tipo"
            raise Exception(msg)
    se[0] = Termino("[" + ", ".join(e.texto for e in se[2]) + "]", "ARR_" + tipo)

def p_arraymember(se):
    """
    arraymember : ID LBRACKET expression RBRACKET
    """
    msg = lineerr(se.lineno(1))
    if se[3].tipo != "NUMBER":
        msg += "el índice del arreglo no es numérico"
        raise Exception(msg)
    msg += se[1] + ": "
    try:
        if not type_by_id[se[1]].startswith("ARR_"):
            raise Exception(msg + "no es un arreglo")
    except KeyError:
        raise Exception(msg + "variable desconocida")
    se[0] = Termino("{}[{}]".format(se[1], se[3].texto), type_by_id[se[1]][4:])


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
                 | ID COLON expression
                 | ID COLON expression COMMA registerlist
    """
    if len(se) == 1: #
        se[0] = []
    elif len(se) == 4: # ID COLON expression
        se[0] = [(se[1], "{}: {}".format(se[1], se[3].texto), se[3].tipo)]
    else: # ID COLON expression COMMA registerlist
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
    unaryop : expression
    """
    # quizas unaryop : op expression


# BINARYOP

def p_binaryop(se): # TODO: hacer algo
    """
    binaryop : expression ADD term
             | expression SUB term
             | term
    """
    if len(se) == 2:
        se[0] = se[1]
    else:
        msg = "{}({}): ".format(lineerr(se.lineno(2)), se[2])
        if se[1].tipo != se[3].tipo:
            raise Exception(msg + "los tipos no coinciden")
        elif se[2] == "+" and se[1].tipo not in ["NUMBER", "STRING"]:
                raise Exception(msg + "se esparaban números o cadenas, se encontró " + se[1].tipo)
        elif se[2] == "-" and se[1].tipo != "NUMBER":
            raise Exception(msg + "se esperaban números")
        se[0] = Termino("{} {} {}".format(se[1].texto, se[2], se[3].texto), "NUMBER")

def p_term(se):
    """
    term : term MULT factor
         | term DIV factor
         | term MOD factor
         | term POW factor
         | factor
    """
    if len(se) == 2:
        se[0] = se[1]
    else:
        msg = "{}({}): ".format(lineerr(se.lineno(2)), se[2])
        if se[1].tipo != se[3].tipo:
            raise Exception(msg + "los tipos no coinciden")
        elif se[1].tipo != "NUMBER":
            raise Exception(msg + "se esperaban números")
        se[0] = Termino("{} {} {}".format(se[1].texto, se[2], se[3].texto), se[1].tipo)

def p_factor(se):
    """
    factor : literal
           | LPARENT expression RPARENT
    """
    if len(se) == 2:
        se[0] = se[1]
    else:
        se[0] = Termino("({})".format(se[2]), "NUMBER")
