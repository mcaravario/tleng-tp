from tokens import *
from expression import *


def tab(s):
    return "".join(["\t" + v for v in s.splitlines(True)])


def err(se):
    return "Error de parseo en línea {0}".format(se.lineno)


def p_error(se):
    if se is None:
        msg = "Parsing error."
    else:
        msg = err(se)
        msg += "\n\trule: " + se.type
        msg += "\n\tsubexpression value: " + se.value
        msg += "\n\tlineno: " + se.lineno
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


# CALL

def p_call(se):
    "call : funname LPARENT termlist RPARENT"
    if se[1] == "multiplicacionEscalar":
        se[1] += "!"
    elif se[1] == "capitalizar":
        se[1] += "!"
    elif se[1] == "colineales":
        se[1] += "!"
    elif se[1] == "print":
        se[1] += "!"
    elif se[1] == "length":
        se[1] += "!"
    else:
        msg = err(se)
        msg += " función desconocida: " + se[1]
        raise Exception(msg)
    se[0] = Instruccion(se[1] + "(" + ", ".join(se[3]) + ")")

def p_funname(se):
    """
    funname : MULTESCALAR
            | CAPITALIZAR
            | COLINEALES
            | PRINT
            | LENGTH
    """
    se[0] = se[1].texto

# def p_call_multescalar2(se):
#     "call : MULTESCALAR LPARENT term COMMA term RPARENT"
#     print("")
#     print(se.__dict__)
#     print("")
#     if se[3].tipo != "ARR_NUMBER":
#         msg = err(se)
#         msg += " se esperaba un arreglo numérico en llamado a " + se[1]
#         raise Exception(msg)
#     if se[5].tipo != "NUMBER":
#         msg = err(se)
#         msg += " se esperaba un número en llamado a " + se[1]
#         raise Exception(msg)
#     se[0] = Instruccion("multiplicacionEscalar(" + se[3].texto + ", " + se[5].texto + ")")

# def p_call_multescalar3(se):
#     "call : MULTESCALAR LPARENT term COMMA term COMMA term RPARENT"
#     if se[3].tipo != "ARR_NUMBER":
#         msg = err(se)
#         msg += " se esperaba un arreglo numérico en llamado a " + se[1]
#         raise Exception(msg)
#     if se[5].tipo != "NUMBER":
#         msg = err(se)
#         msg += " se esperaba un número en llamado a " + se[1]
#         raise Exception(msg)
#     if se[7].tipo != "BOOL":
#         msg = err(se)
#         msg += " se esperaba un número en llamado a " + se[1]
#         raise Exception(msg)
#     se[0] = Instruccion(se[1] + "(" + se[3].texto + ", " + se[5].texto + ")")


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

def p_term_number(se):
    "term : NUMBER"
    se[0] = Termino(se[1], "NUMBER")

def p_term_string(se):
    "term : STRING"
    se[0] = Termino(se[1], "STRING")

def p_term_true(se):
    "term : TRUE"
    se[0] = Termino(se[1], "BOOL")

def p_term_false(se):
    "term : FALSE"
    se[0] = Termino(se[1], "BOOL")

def p_term_id(se):
    "term : ID"
    se[0] = Termino(se[1], "UNKNOWN")

def p_term_res(se):
    "term : RES"
    se[0] = Termino(se[1], "UNKNOWN")

def p_term_register(se):
    "term : ID DOT ID"
    se[0] = Termino(se[1] + "." + se[3], "UNKNOWN")

def p_term_paren(se):
    "term : LPARENT term RPARENT"
    se[0] = Termino("(" + se[2].texto + ")", se[2].tipo)

def p_term_index(se):
    "term : ID LBRACKET term RBRACKET"
    se[0] = Termino(se[1] + "[" + se[3].texto + "]", "UNKNOWN")

def p_termlist(se):
    """
    termlist :
             | term
             | term COMMA termlist
    """
    if len(se) == 1:
        se[0] = []
    elif len(se) == 2:
        se[0] = [se[1]]
    elif len(se) == 4:
        se[0] = [se[1]] + se[3]

def p_term_array(se):
    "term : LBRACKET termlist RBRACKET"
    if len(se[2]) == 0:
        tipo = "UNKNOWN"
    else:
        tipo = se[2][0].tipo
        if any(e.tipo != tipo for e in se[2]):
            msg = err(se)
            msg += " los elementos del arreglo no son del mismo tipo."
            raise Exception(msg)
    se[0] = Termino("[" + ", ".join(e.texto for e in se[2]) + "]", "ARR_" + tipo)

# def p_expression_algo(se):
#     "expression : term"
#     se[0] = se[1]

