from tokens import *
from expression import *

def p_arithmetic_add(subexpr):
    'ari_a : ari_a ADD ari_t'
    if subexpr[1].tipo != subexpr[3].tipo:
        raise Exception('NO ESTAN BIEN LOS TIPOS')
    subexpr[0] = Termino(subexpr[1].texto + ' + ' + subexpr[3].texto, 'INT')
    
def p_arithmetic_a_t(subexpr):
    'ari_a : ari_t' 
    subexpr[0] = subexpr[1]

def p_arithmetic_mult(subexpr):
    'ari_t : ari_t MULT ari_f'
    subexpr[0] = Termino(subexpr[1].texto + ' * ' + subexpr[3].texto, 'INT')

def p_arithmetic_t_f(subexpr):
    'ari_t : ari_f' 
    subexpr[0] = subexpr[1]

def p_arithmetic_f_term(subexpr):
    'ari_f : term'
    subexpr[0] = subexpr[1]

def p_ari_pa(subexpr):
    'ari_f : LPARENT ari_a RPARENT'
    subexpr[0] = Termino('(' + subexpr[2].texto + ')', 'INT')

def p_error(subexpr):
    raise Exception("Syntax error.")

def p_term_number(subexpr):
    'term : NUMBER'
    subexpr[0] = Termino(subexpr[1],'INT')

def p_term_string(subexpr):
    'term : STRING'
    subexpr[0] = Termino(subexpr[1], 'STRING')

def p_term_true(subexpr):
    'term : TRUE'
    subexpr[0] = Termino(subexpr[1],'BOOL')

def p_term_false(subexpr):
    'term : FALSE'
    subexpr[0] = Termino(subexpr[1],'BOOL')

def p_term_id(subexpr):
    'term : ID'
    subexpr[0] = Termino(subexpr[1],'UNKNOWN')

def p_term_res(subexpr):
    'term : RES'
    subexpr[0] = Termino(subexpr[1],'UNKNOWN')

def p_term_register(subexpr):
    'term : ID DOT ID'
    subexpr[0] = Termino(subexpr[1]+'.'+subexpr[3],'UNKNOWN')

def p_term_paren(subexpr):
    'term : LPARENT term RPARENT'
    subexpr[0] = Termino('('+subexpr[2].texto+')',subexpr[2].tipo)
    
def p_term_index(subexpr):
    'term : ID LBRACKET ari_a RBRACKET'
    subexpr[0] = Termino(subexpr[1] + '['+subexpr[3].texto+']','UNKNOWN')

# def p_expression_algo(subexpr):
#     'expression : term'
#     subexpr[0] = subexpr[1]

