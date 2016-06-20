from tokens import *
from expression import *


def err(se):
    return "Error de parseo en línea {0}".format(se.lineno)


def p_error(se):
    if se is None:
        msg = "Parsing error."
    else:
        msg = err(se)
        msg += "\n\trule: " + se.type
        msg += "\n\tsubexpression value: " + se.value
    raise Exception(msg)


# STMT

def p_stmt(se):
    """
    stmt :
         | COMMENT stmt
         | assign SEMICOLON stmt
         | call SEMICOLON stmt
    """
    if len(se) == 1: # vacio
        se[0] = Declaracion("")
    elif len(se) == 3: # comentario
        se[0] = Declaracion(se[1] + "\n" + se[2].texto)
    elif len(se) == 4: # assign | call
        se[0] = Declaracion(se[1].texto + ";\n" + se[3].texto)


# ASSIGN

def p_assign(se):
    "assign : ID ASSIGN term"
    se[0] = Declaracion(se[1] + " = " + se[3].texto)


# ARI

def p_ari_add(se):
    "ari_a : ari_a ADD ari_t"
    if se[1].tipo != se[3].tipo:
        raise Exception("NO ESTAN BIEN LOS TIPOS")
    se[0] = Termino(se[1].texto + " + " + se[3].texto, "INT")

def p_ari_a2t(se):
    "ari_a : ari_t"
    se[0] = se[1]

def p_ari_mult(se):
    "ari_t : ari_t MULT ari_f"
    se[0] = Termino(se[1].texto + " * " + se[3].texto, "INT")

def p_ari_t2f(se):
    "ari_t : ari_f"
    se[0] = se[1]

def p_ari_f2term(se):
    "ari_f : term"
    se[0] = se[1]

def p_ari_parens(se):
    "ari_f : LPARENT ari_a RPARENT"
    se[0] = Termino("(" + se[2].texto + ")", "INT")


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
    "term : ID LBRACKET ari_a RBRACKET"
    se[0] = Termino(se[1] + "[" + se[3].texto + "]", "UNKNOWN")

def p_termlist(se):
    """
    termlist :
             | term
             | termchain termlist
    """
    if len(se) == 1:
        se[0] = []
    elif len(se) == 2:
        se[0] = [se[1]]
    elif len(se) == 3:
        se[0] = [se[1]] + se[2]

def p_termchain(se):
    "termchain : term COMMA"
    se[0] = se[1]

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

