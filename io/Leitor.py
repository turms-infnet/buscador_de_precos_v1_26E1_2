from .IO import IO
from csv import DictReader

class Leitor(IO):
    def __init__(self, arquivo, separador=";"):
        super().__init__(arquivo, separador)

    def ler_arquivo(self):
        resultados = []
        with open(self.arquivo,  mode="r", encoding="utf-8") as _arquivo:
            leitor = DictReader(_arquivo, delimiter=self.separador)
            for linha in leitor:
                resultados.append(linha)
        return resultados