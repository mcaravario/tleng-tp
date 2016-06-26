class Termino(object):
    def __init__(self, texto, tipo, tiposreg = None):
        self.texto = texto
        self.tipo  = tipo
        self.tiposreg = tiposreg

class Instruccion(object):
    def __init__(self, texto):
        self.texto = texto
