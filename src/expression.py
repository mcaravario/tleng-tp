class Termino(object):
    def __init__(self, texto, tipo):
        self.texto = texto
        if type(tipo) is not tuple:
            raise Exception("no tipa! pasa una tupla!")
        self.tipo = tipo

class Instruccion(object):
    def __init__(self, texto):
        self.texto = texto

class Bloque(object):
    def __init__(self, texto, commb="", comme=""):
        self.texto = texto
        self.comentarios = (str(commb), str(comme))
