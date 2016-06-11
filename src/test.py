import lexer_rules
import parser_rules
from ply.lex import lex
from ply.yacc import yacc
lexer = lex(module=lexer_rules)
parser = yacc(module=parser_rules)
text = "marto[3+4+(5+6)*8+2]"
res = parser.parse(text, lexer)
print(res.__dict__)
