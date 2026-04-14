import os
from dotenv import load_dotenv
from extrator import ExtratorAmazon, ExtratorAmericanas, ExtratorMercadoLivre
import logging
from FileProcessor import Leitor, Escritor
# import sentry_sdk

from notificacao import Email

logging.basicConfig(
    filename="server.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s no arquivo %(filename)s e função %(funcName)s na linha %(lineno)d: %(message)s",
)

# sentry_sdk.init(
#     dsn=os.getenv("SENTRY_DSN"),
#     send_default_pii=os.getenv("SEND_DEFAULT_PII"),
# )

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD_APP = os.getenv("PASSWORD_APP")



def main():
    carteiro = Email(EMAIL, PASSWORD_APP, logging)

    leitorProdutos = Leitor("data/produtos.csv")
    leitorClientes = Leitor("data/clientes.csv")
    escritorProdutosEncontrados = Escritor("data/produtos_encontrados.csv")

    lista_clientes = leitorClientes.ler_arquivo()
    lista_produtos = leitorProdutos.ler_arquivo()

    lista_produtos_atualizados = []

    for produto in lista_produtos:
        nome = produto["produto"]
        extratorMl = ExtratorMercadoLivre(nome, logging)
        produtoMl = extratorMl.buscar_produto()

        extratorAm = ExtratorAmazon(nome, logging)
        produtoAm = extratorAm.buscar_produto()

        extratorAme = ExtratorAmericanas(nome, logging)
        produtoAme = extratorAme.buscar_produto()

        precoMl = produtoMl["preco"]
        precoAm = produtoAm["preco"]
        precoAme = produtoAme["preco"]

        if precoMl < precoAm and precoMl < precoAme and precoMl != "0.00":
            lista_produtos_atualizados.append(produtoMl)
        elif precoAm < precoMl and precoAm < precoAme and precoAm != "0.00":
            lista_produtos_atualizados.append(produtoAm)
        elif precoAme !="0.00" :
            lista_produtos_atualizados.append(produtoAme)

        lista_produtos_atualizados[-1]["id_produto"] = produto["id"]
        lista_produtos_atualizados[-1].update({"nome": nome})
    
    escritorProdutosEncontrados.escrever_arquivo(lista_produtos_atualizados)

    for cliente in lista_clientes:
        email = cliente["email"]
        ids_produtos = cliente["id_produtos"].split(",")
        oferta_cliente = []
        for produto in lista_produtos_atualizados:
            if produto["id_produto"] in ids_produtos:
                oferta_cliente.append(produto)
        
        carteiro.enviar_email(email, oferta_cliente)


if __name__ == "__main__":
    main()