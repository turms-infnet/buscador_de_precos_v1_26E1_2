from abc import ABC

class FileProcessor(ABC):
    def __init__(self, arquivo, separador=";"):
        self.arquivo = arquivo
        self.separador = separador
