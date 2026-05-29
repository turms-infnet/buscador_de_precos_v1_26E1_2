import os
from dotenv import load_dotenv
from extrator import ExtratorAmazon, ExtratorAmericanas, ExtratorMercadoLivre
import logging
from FileProcessor import Leitor, Escritor
from create_db import (
    select_clientes, 
    select_produtos, 
    select_cliente_produtos, 
    salvar_precos_encontrados
)
from selenium.webdriver.common.by import By

from notificacao import Email

logging.basicConfig(
    filename="server.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s no arquivo %(filename)s e função %(funcName)s na linha %(lineno)d: %(message)s",
)

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD_APP = os.getenv("PASSWORD_APP")

def main():
    carteiro = Email(EMAIL, PASSWORD_APP, logging)

    lista_clientes = select_clientes(logging)
    lista_produtos = select_produtos(logging)

    lista_produtos_atualizados = []

    for produto in lista_produtos:
        nome = produto.nome
        extratorMl = ExtratorMercadoLivre(nome, logging, {
            "select": {
                "type": By.CSS_SELECTOR,
                "name": "button[class='andes-dropdown__trigger']"
            },
            "option": {
                "type": By.CSS_SELECTOR,
                "name": "li.andes-list__item.andes-list__item--size-medium:nth-of-type(2)"
            },
            "item": "ui-search-result__wrapper",
            "price": "andes-money-amount__fraction",
            "link": "poly-component__title"
        })
        produtoMl = extratorMl.buscar_produto()

        # extratorAm = ExtratorAmazon(nome, logging)
        # produtoAm = extratorAm.buscar_produto()

        # extratorAme = ExtratorAmericanas(nome, logging)
        # produtoAme = extratorAme.buscar_produto()
        # 

        produtoMl.id = produto.id
        lista_produtos_atualizados.append(produtoMl)

        # precoMl = produtoMl.preco                                 
        # precoAm = produtoAm.preco
        # precoAme = produtoAme.preco)
        # if precoMl < precoAm and precoMl < precoAme and precoMl != "0.00":
        #     produtoMl.id = produto.id
        #     lista_produtos_atualizados.append(produtoMl)
        # elif precoAm < precoMl and precoAm < precoAme and precoAm != "0.00":
        #     produtoAm.id = produto.id
        #     lista_produtos_atualizados.append(produtoAm)
        # elif precoAme !="0.00" :
        #     produtoAme.id = produto.id
        #     lista_produtos_atualizados.append(produtoAme)
    
    salvar_precos_encontrados(lista_produtos_atualizados, logging)

    # lista_clientes = select_clientes(logging)
    for cliente in lista_clientes:
        carteiro.enviar_email(cliente.email, cliente.produtos[0])


if __name__ == "__main__":
    main()