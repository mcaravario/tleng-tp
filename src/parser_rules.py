from tokens import *
from expression import *


def p_error(se):
    msg = "Parsing error @ line {0}, column {1}:".format(se.lineno, se.lexpos + 1)
    msg += "\n\trule: " + se.type
    msg += "\n\tsubexpression value: " + se.value
    raise Exception(msg)


# ARI

def p_ari_add(se):
    "ari_a : ari_a ADD ari_t"
    if se[1].tipo != se[3].tipo:
        raise Exception("NO ESTAN BIEN LOS TIPOS")
    se[0] = Termino(se[1].texto + " + " + se[3].texto, "INT")

def p_ari_a_t(se):
    "ari_a : ari_t"
    se[0] = se[1]

def p_ari_mult(se):
    "ari_t : ari_t MULT ari_f"
    se[0] = Termino(se[1].texto + " * " + se[3].texto, "INT")

def p_ari_t_f(se):
    "ari_t : ari_f"
    se[0] = se[1]

def p_ari_f_term(se):
    "ari_f : term"
    se[0] = se[1]

def p_ari_pa(se):
    "ari_f : LPARENT ari_a RPARENT"
    se[0] = Termino("(" + se[2].texto + ")", "INT")


# TERM

def p_term_number(se):
    "term : NUMBER"
    se[0] = Termino(se[1],"INT")

def p_term_string(se):
    "term : STRING"
    se[0] = Termino(se[1], "STRING")

def p_term_true(se):
    "term : TRUE"
    se[0] = Termino(se[1],"BOOL")

def p_term_false(se):
    "term : FALSE"
    se[0] = Termino(se[1],"BOOL")

def p_term_id(se):
    "term : ID"
    se[0] = Termino(se[1],"UNKNOWN")

def p_term_res(se):
    "term : RES"
    se[0] = Termino(se[1],"UNKNOWN")

def p_term_register(se):
    "term : ID DOT ID"
    se[0] = Termino(se[1] + "." + se[3],"UNKNOWN")

def p_term_paren(se):
    "term : LPARENT term RPARENT"
    se[0] = Termino("(" + se[2].texto + ")",se[2].tipo)

def p_term_index(se):
    "term : ID LBRACKET ari_a RBRACKET"
    se[0] = Termino(se[1] + "[" + se[3].texto + "]","UNKNOWN")

# def p_expression_algo(se):
#     "expression : term"
#     se[0] = se[1]

