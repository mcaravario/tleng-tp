# -*- coding: utf-8 -*-
from tokens import *
from expression import *


type_by_id = {}
register_types = {}


def tab(s):
    return "".join(["\t" + v for v in s.splitlines(True)])


def lineerr(n):
    return "Error de parseo en línea {}: ".format(n)

def formatBlock(t):
    if type(t) is Bloque:
        return " {" + t.comentarios[0] + "\n" + tab(t.texto) + "}" + t.comentarios[1] + "\n"
    else:
        return "\n" + tab(t.texto)

def p_error(se):
    if se is None:
        msg = "Parsing error."
    else:
        msg = lineerr(se.lineno)
        msg += "\n\trule: " + se.type
        if type(se.value) is tuple:
            msg += "\n\tsubexpression value: " + se.value[0]
        else:
            msg += "\n\tsubexpression value: " + se.value
        msg += "\n\tlineno: " + str(se.lineno)
    raise Exception(msg)


# INSTR

def p_instrlist(se):
    """
    instrlist : instaux
              | instaux instrlist
    """
    if len(se) == 2: # instr
        se[0] = se[1]
    else:
        se[0] = Instruccion(se[1].texto + se[2].texto)

def p_instr(se):
    """
    instr : commentlist instrop maybeinlcomment
    """
    if len(se) == 4:
        se[0] = Instruccion(se[1] + se[2].texto + se[3] + "\n")

def p_commentlist(se):
    """
    commentlist :
                | COMMENT commentlist
    """
    if len(se) == 3: # COMMENT commentlist
        se[0] = se[1] + "\n" + se[2]
    else: #
        se[0] = ""

def p_maybeinlcomment(se):
    """
    maybeinlcomment :
                    | INLCOMMENT
    """
    if len(se) == 2: # INLCOMMENT
        se[0] = " " + se[1]
    else: #
        se[0] = ""

def p_instrop(se):
    """
    instrop : assign SEMICOLON
            | unarymod SEMICOLON
            | call SEMICOLON
            | RETURN expression SEMICOLON
            | loop
    """
    if len(se) == 2 and (type(se[1]) is Instruccion): # loop
        se[0] = Instruccion(se[1].texto)
    elif len(se) == 3: # assign SEMICOLON | call SEMICOLON
        se[0] = Instruccion(se[1].texto + ";")
    else: ## RETURN expression SEMICOLON
        se[0] = Instruccion("{} {};".format(se[1],se[2].texto))

def p_instropfor(se):
    """
    instropfor :
               | assign
               | unarymod
               | call
    """
    if len(se) == 2:
        se[0] = Instruccion(se[1].texto)
    else:
        se[0] = Instruccion("")

def p_block(se):
    """
    block : instr
          | LBRACE maybeinlcomment instrlist RBRACE maybeinlcomment
    """
    if len(se) == 2: # instr
        se[0] = Instruccion(se[1].texto)
    else: # LBRACE maybeinlcomment instrlist RBRACE maybeinlcomment
        se[0] = Bloque(se[3].texto, se[2], se[5])

def p_blockaux(se):
    """
    blockaux : instrop
             | LBRACE instrlist RBRACE
    """
    if len(se) == 2: # instr
        se[0] = Instruccion(se[1].texto)
    else: # LBRACE instrlist RBRACE
        se[0] = Bloque(se[2].texto)

# CONDITIONALS

def p_instaux(se):
    """
    instaux : mconditional
            | oconditional
    """
    se[0] = se[1]

def p_mconditional(se):
    """
    mconditional : IF LPARENT expression RPARENT mconditional ELSE mconditional
                 | block
    """
    if len(se) == 2:
        se[0] = se[1]
    else:
        se[0] = Instruccion("if ({}){}else {}".format(se[3].texto,formatBlock(se[5]),formatBlock(se[7])))


def p_oconditional(se):
    """
    oconditional : IF LPARENT expression RPARENT mconditional ELSE oconditional
                 | IF LPARENT expression RPARENT instaux
    """
    if len(se) == 6:
        se[0] = Instruccion("if ({}){}".format(se[3].texto, formatBlock(se[5])))
    else:
        se[0] = Instruccion("if ({}){}else{}".format(se[3].texto,formatBlock(se[5]),formatBlock(se[7])))

# LOOP

def p_loop(se):
    """
    loop : FOR LPARENT instropfor SEMICOLON expression SEMICOLON instropfor RPARENT blockaux
         | WHILE LPARENT expression RPARENT blockaux
         | DO block WHILE LPARENT expression RPARENT SEMICOLON
    """
    if len(se) == 10: # FOR LPARENT instropfor SEMICOLON expression SEMICOLON instropfor RPARENT block
        se[0] = Instruccion("for ({}; {}; {}){}".format(se[3].texto,
                                                        se[5].texto,
                                                        se[7].texto,
                                                        formatBlock(se[9])))
    elif len(se) == 6: # WHILE LPARENT expression RPARENT block
        se[0] = Instruccion("while ({}) {}".format(se[3].texto, formatBlock(se[5])))
    else: # DO block WHILE LPARENT expression RPARENT SEMICOLON
        # esto no puede generar una excepción IndexError, pues los terminos son
        # no vacios y los bloques siempre terminan en '\n'
        if se[2].texto[-2] == "}":
            se[0] = Instruccion("do {} while ({});\n".format(formatBlock(se[2]).rstrip(), se[5].texto))
        else:
            se[0] = Instruccion("do {}while ({});\n".format(formatBlock(se[2]), se[5].texto))

# ASSIGN

def p_assign_number(se):
    """
    assignop : ADDEQ
             | SUBEQ
             | DIVEQ
             | MULTEQ
    """
    se[0] = se[1]

def p_opassign(se):
    """
    assign : ID assignop expression
           | arraymember assignop expression
           | registermember assignop expression
    """
    if type(se[1]) is Termino: # arraymember ASSIGN expression | registermember ASSIGN expression
        msg = "{}{}: ".format(lineerr(se.lineno(1)), se[2])
        if se[2] == "+=" and not (se[1].tipo in ["NUMBER", "STRING"]):
            msg += "se esperaba un tipo numérico o string para +="
            raise Exception(msg)
        elif s[2] in ["-=","*=","/="] and not (se[1].tipo == "NUMBER"):
            msg += "se esperaba un tipo numérico para " ++ se[2];
            raise Exception(msg)
        se[0] = Instruccion("{} {} {}".format(se[1].texto,se[2],se[3].texto))
    else:
        msg = "{}{}: ".format(lineerr(se.lineno(1)), se[1])
        if se[1] not in type_by_id:
            raise Exception(msg + "variable no declarada")
        msg = lineerr(se.lineno(1))
        tipo = type_by_id.get(se[1])
        if tipo != se[3].tipo:
            msg += "el tipo de la variable " + se[2] + "no coincide con el"
            msg += "tipo de la expresion"
            raise Exception(msg)
        if se[2] == "+=" and tipo not in ["NUMBER", "STRING"]:
            msg += "se esperaba un tipo numérico o string para +="
            raise Exception(msg)
        elif se[2] != "+=" and tipo != "NUMBER":
            msg += "se esperaba un tipo numérico para " + se[2];
            raise Exception(msg)
        se[0] = Instruccion("{} {} {}".format(se[1],se[2],se[3].texto))

'''
def p_maybeassign(se):
    """
    maybeassign  :
                 | assign
    """
    if len(se) == 2:
        se[0] = Instruccion(se[1].texto)
    else:
        se[0] = Instruccion("")
'''
def p_assign(se):
    """
    assign : ID ASSIGN expression
           | arraymember ASSIGN expression
           | registermember ASSIGN expression
    """
    if type(se[1]) is Termino: # arraymember ASSIGN expression | registermember ASSIGN expression
        msg = lineerr(se.lineno(2))
        if(se[1].tipo != se[3].tipo):
            msg += "el tipo del arreglo de la variable " + se[1].texto + "no coincide con el"
            msg += "tipo de la expresion"
            raise Exception(msg)
        se[0] = Instruccion("{} {} {}".format(se[1].texto,se[2],se[3].texto))
    else:
        type_by_id[se[1]] = se[3].tipo
        if(se[3].tipo == 'REGISTER'):
            register_types[se[1]] = se[3].tiposreg
        se[0] = Instruccion("{} {} {}".format(se[1],se[2],se[3].texto))

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
        tipo = "ARR_NUMBER"
        if len(se[3]) != 2 and len(se[3]) != 3:
            raise Exception(msg + "se esparaban 2 o 3 parámetros")
        if se[3][0].tipo != "ARR_NUMBER":
            raise Exception(msg + "se esperaba un arreglo numérico")
        if se[3][1].tipo != "NUMBER":
            raise Exception(msg + "se esparaba un escalar")
        if len(se[3]) == 3 and se[3][2].tipo != "BOOL":
            raise Exception(msg + "se esperaba un booleano")
    elif se[1] == "capitalizar":
        tipo = "STRING"
        if len(se[3]) != 1:
            raise Exception(msg + "se esperaba un parámetro")
        if se[3][0].tipo != "STRING":
            raise Exception(msg + "se esperaba una cadena")
    elif se[1] == "colineales":
        tipo = "BOOL"
        if len(se[3]) != 2:
            raise Exception(msg + "se esperaban 2 parámetros")
        if se[3][0].tipo != "ARR_NUMBER" or se[3][1].tipo != "ARR_NUMBER":
            raise Exception(msg + "se esperaban arreglos numéricos")
    elif se[1] == "print":
        tipo = "PRINT"
        if len(se[3]) != 1:
            raise Exception(msg + "se esperaba un parámetro")
    elif se[1] == "length":
        tipo = "NUMBER"
        if len(se[3]) != 1:
            raise Exception(msg + "se esperaba un parámetro")
        if se[3][0].tipo != "STRING" and not se[3][0].tipo.startswith("ARR_"):
            raise Exception(msg + "se esperaba una cadena o un arreglo")
    else:
        raise Exception(msg + "función desconocida")
    se[0] = Termino("{}({})".format(se[1], ", ".join(t.texto for t in se[3])), tipo)


# TERM
'''
def p_maybeexpr(se):
    """
    maybeexpr :
              | expression
    """
    if len(se) == 2:
        se[0] = Termino(se[1].texto, se[1].tipo)
    else:
        se[0] = Termino("",None)
'''
def p_expression(se):
    """
    expression : array
               | register
               | lbinaryop
               | expression QUESTION expression COLON lcomp
    """
    if len(se) == 6: # LPARENT expression RPARENT QUESTION expression COLON expression
        msg = lineerr(se.lineno(2))
        if se[1].tipo != "BOOL":
            msg += "se esperaba una expresión booleana"
            raise Exception(msg)
        elif se[3].tipo != se[5].tipo:
            msg += "las ramas del operador ?: deben tener el mismo tipo"
            raise Exception(msg)
        se[0] = Termino("{} ? {} : {}".format(se[1].texto, se[3].texto, se[5].texto), se[3].tipo)
    else: # register | array | binaryop
        se[0] = se[1]

def p_literal(se):
    """
    literal : NUMBER
            | STRING
            | FALSE
            | TRUE
    """
    se[0] = Termino(se[1][0],se[1][1])


def p_expressionlist(se):
    """
    expressionlist : expression
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
    arraymember : var LBRACKET expression RBRACKET
    """
    msg = lineerr(se.lineno(1))
    if se[3].tipo != "NUMBER":
        msg += "el índice del arreglo no es numérico"
        raise Exception(msg)
    msg += se[1].texto + ": "
    if not se[1].tipo.startswith("ARR_"):
        raise Exception(msg + "no es un arreglo")
    se[0] = Termino("{}[{}]".format(se[1].texto, se[3].texto), se[1].tipo[4:])


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
    reg = register_types.get(se[1])
    if reg is None:
        msg = "{}{}: ".format(lineerr(se.lineno(1)), se[1])
        if se[1] not in type_by_id:
            raise Exception(msg + " registro no declarada")
    tipo = reg.get(se[3])
    if tipo is None:
        msg = "{}: ".format(lineerr(se.lineno(1)))
        raise Exception(msg + "campo {} del registro {} no declarada".format(se[3],se[1]))
    se[0] = Termino("{}.{}".format(se[1], se[3]), tipo)



def p_lbinaryop(se):
    """
    lbinaryop : expression AND lcomp
              | expression OR lcomp
              | lcomp
    """
    if(len(se) == 2):
        se[0] = se[1]
    else:
        if(se[1].tipo != "BOOL" or se[3].tipo != "BOOL"):
            msg = "{}: ".format(lineerr(se.lineno(1)))
            raise Exception(msg + "se esperaban dos bools")
        se[0] = Termino("{} {} {}".format(se[1].texto, se[2], se[3].texto), "BOOL")

def p_lcomp(se):
    """
    lcomp : lcomp LEQ    binaryop
          | lcomp GEQ    binaryop
          | lcomp LT     binaryop
          | lcomp GT     binaryop
          | lcomp EQUAL  binaryop
          | lcomp LNOTEQ binaryop
          | binaryop
    """
    if(len(se) == 2): # binaryop
        se[0] = se[1]
    elif se[2] in ["==", "!="]: # ==, !=
        if(se[1].tipo != se[3].tipo):
            msg = "{} {}: ".format(lineerr(se.lineno(2)),se[2])
            raise Exception(msg + "los tipos no coinciden")
        se[0] = Termino("{} {} {}".format(se[1].texto,se[2],se[3].texto),"BOOL")
    else: # <=, >=, <, >
        if(se[1].tipo != "NUMBER" or se[3].tipo != "NUMBER"):
            msg = "{} {}: ".format(lineerr(se.lineno(2)),se[2])
            raise Exception(msg + "se esperaban dos numeros")
        se[0] = Termino("{} {} {}".format(se[1].texto,se[2],se[3].texto),"BOOL")


def p_binaryop(se):
    """
    binaryop : binaryop ADD term
             | binaryop SUB term
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
        se[0] = Termino("{} {} {}".format(se[1].texto, se[2], se[3].texto), se[1].tipo)

def p_term(se):
    """
    term : term MULT unaryop
         | term DIV unaryop
         | term MOD unaryop
         | term POW unaryop
         | unaryop
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

# UNARYOP
def p_unarymod(se):
    """
    unarymod : INC var
             | DEC var
             | var INC
             | var DEC
    """
    if(type(se[1]) is Termino):
        msg = "{}: ".format(lineerr(se.lineno(1)))
        if se[1].tipo != "NUMBER":
            raise Exception(msg + " se esperaba numérico para" ++ se[1])
        se[0] = Termino(se[1].texto + se[2],se[1].tipo)
    else:
        msg = "{}: ".format(lineerr(se.lineno(1)))
        if se[2].tipo != "NUMBER":
            raise Exception(msg + " se esperaba numérico para" ++ se[1])
        se[0] = Termino(se[1] + se[2].texto,se[2].tipo)

def p_unaryop(se):
    """
    unaryop : ADD unaryop
            | SUB unaryop
            | NOT unaryop
            | unarymod
            | factor
    """
    if len(se) == 2:
        se[0] = se[1]
    else:
        if se[1] == "NOT":
            msg = "{}: ".format(lineerr(se.lineno(1)))
            if se[2].tipo != "BOOL":
                raise Exception(msg + " se esperaba tipo bool para NOT")
            se[0] = Termino("{} {}".format(se[1], se[2].texto), se[2].tipo)
        elif se[1] != "NOT":
            msg = "{}: ".format(lineerr(se.lineno(1)))
            if se[2].tipo != "NUMBER":
                raise Exception(msg + " se esperaba numérico para" ++ se[1])
            se[0] = Termino("{}{}".format(se[1], se[2].texto), se[2].tipo)


def p_var(se):
    """
    var : ID
        | RES
        | arraymember
        | registermember
    """
    if type(se[1]) is Termino: # arraymember | registermember
        se[0] = se[1]
    else: ## ID | RES
        msg = "{}{}: ".format(lineerr(se.lineno(1)), se[1])
        if se[1] not in type_by_id:
            raise Exception(msg + "variable no declarada")
        se[0] = Termino(se[1], type_by_id[se[1]], register_types.get(se[1]))

def p_factor(se):
    """
    factor : literal
           | var
           | call
           | LPARENT expression RPARENT
    """
    if len(se) == 2:
        se[0] = se[1]
        if(type(se[1]) is Termino and se[1].tipo == "PRINT"): ## Ej: a=print("hola");
            msg = lineerr(se.lineno(1))
            raise Exception(msg + "print no devuelve un valor")
    else:
        se[0] = Termino("( {} )".format(se[2].texto), se[2].tipo)
