import os
from .IO import IO

class Escritor(IO):
    def __init__(self, arquivo, separador=";"):
        self.super(arquivo, separador)
    
    def escrever_arquivo(self, resultados):
        exists = os.path.exists(self.arquivo)
        if exists:
            os.remove(self.arquivo)

        with open(self.arquivo, mode="w", encoding="utf-8", newline="") as _arquivo:
            for item in resultados:
                pass
        