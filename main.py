import os
from dotenv import load_dotenv
from extrator import ExtratorAmazon, ExtratorAmericanas, ExtratorMercadoLivre
import logging
from FileProcessor import Leitor, Escritor
from database.connection import (
    open_connection, 
    select_clientes, 
    select_produtos, 
    select_cliente_produtos, 
    salvar_precos_encontrados
)
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

def main(conn):
    carteiro = Email(EMAIL, PASSWORD_APP, logging)

    lista_clientes = select_clientes(conn, logging, True)
    lista_produtos = select_produtos(conn, logging, True)

    lista_produtos_atualizados = []

    for produto in lista_produtos:
        nome = produto["nome"]
        extratorMl = ExtratorMercadoLivre(nome, logging)
        produtoMl = extratorMl.buscar_produto()

        extratorAm = ExtratorAmazon(nome, logging)
        produtoAm = extratorAm.buscar_produto()

        extratorAme = ExtratorAmericanas(nome, logging)
        produtoAme = extratorAme.buscar_produto()

        precoMl = produtoMl[1]
        precoAm = produtoAm[1]
        precoAme = produtoAme[1]

        if precoMl < precoAm and precoMl < precoAme and precoMl != "0.00":
            lista_produtos_atualizados.append(produtoMl)
        elif precoAm < precoMl and precoAm < precoAme and precoAm != "0.00":
            lista_produtos_atualizados.append(produtoAm)
        elif precoAme !="0.00" :
            lista_produtos_atualizados.append(produtoAme)

        lista_produtos_atualizados[-1][0] = produto["id_produto"]
        lista_produtos_atualizados[-1].append(nome)
    
    salvar_precos_encontrados(lista_produtos_atualizados)

    for cliente in lista_clientes:
        email = cliente["email"]
        ids_produtos = select_cliente_produtos(conn, cliente["id_cliente"], logging, False)
        oferta_cliente = []
        for produto in lista_produtos_atualizados:
            if produto[0] in ids_produtos:
                oferta_cliente.append(produto)
        
        carteiro.enviar_email(email, oferta_cliente)


if __name__ == "__main__":
    conn = open_connection()
    main(conn)
    conn.close()