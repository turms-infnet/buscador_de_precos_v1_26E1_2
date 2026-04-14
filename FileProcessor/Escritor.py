import os
from .FileProcessor import FileProcessor
from csv import DictWriter

class Escritor(FileProcessor):
    def __init__(self, arquivo, separador=";", colunas=None):
        super().__init__(arquivo, separador)
        self.colunas = colunas
    
    def escrever_arquivo(self, resultados):
        exists = os.path.exists(self.arquivo)
        if exists:
            os.remove(self.arquivo)

        with open(self.arquivo, mode="w", encoding="utf-8", newline="") as _arquivo:
            if self.colunas is None:
                self.colunas = resultados[0].keys()

            escritor = DictWriter(
                _arquivo, fieldnames=self.colunas, delimiter=self.separador
            )
            escritor.writeheader()
            escritor.writerows(resultados)