import lexer_rules
from ply.lex import lex

text = "{  alumno.nombre    = \" Marto Caravario \", alumno.edad  =  23}"
lexer = lex(module=lexer_rules)
lexer.input(text)
token = lexer.token()
while token is not None:
  print(token.value)
  token = lexer.token()
