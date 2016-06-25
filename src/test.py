import lexer_rules
import parser_rules

from ply.lex import lex
from ply.yacc import yacc

lexer = lex(module=lexer_rules)
parser = yacc(module=parser_rules)

# text = "qwe=1;qwe=2;sarasa(qwe[2+3+(4+5)*6+7]);"
text = """
qwe=1.123;asd=["qwe","zxc"]; # mira! comentario!; esto="no anda"; # comentario dentro de comentario?
zxc=0.0;
a=[];
b=[1, 1.0];
if(a)qwe=1.0;qwe=2.0;
if(a)qwe=1.0;else zxc=1.0;
if(a){qwe=1.0;zxc=1;if(b)qwe=2.0;}else qwe=0.0;
if(a){qwe=1.0;zxc=1;if(b)qwe=2.0;}else{qwe=0.0;asd=3.0;}
for(i=0;i;i)qwe=2.0;
for(i=0;i;i){qwe=2.0;asd=1.0;}
while(i)qwe=2.0;
while(i){qwe=2.0;asd=1.0;}
do qwe=2.0; while(i);
do{qwe=2.0;asd=1.0;}while(i);
# c=[1, "qwe"];
# a={"qwe": 123, "zxc": "qwerty"};

"""

# lexer.input(text)
# for tok in lexer:
#     print(tok)

res = parser.parse(text, lexer)
print(res.__dict__)
print("\n" + res.texto)
