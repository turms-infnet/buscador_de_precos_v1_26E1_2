from abc import ABC

class IO(ABC):
    def __init__(self, arquivo, separador=";"):
        self.arquivo = arquivo
        self.separador = separador
