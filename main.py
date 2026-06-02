import os
from dotenv import load_dotenv
from extrator import ExtratorAmazon, ExtratorAmericanas, ExtratorMercadoLivre
import logging
from FileProcessor import Leitor, Escritor
from create_db import (
    select_clientes, 
    select_produtos, 
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
        precoMl = extratorMl.buscar_produto()

        # extratorAm = ExtratorAmazon(nome, logging)
        # precoAm = extratorAm.buscar_produto()

        # extratorAme = ExtratorAmericanas(nome, logging, {})
        # precoAme = extratorAme.buscar_produto()

        precoMl.id_produto = produto.id
        lista_produtos_atualizados.append(precoMl)

        # precoMl = precoMl.preco                                 
        # precoAm = precoAm.preco
        # precoAme = precoAme.preco)
        # if precoMl < precoAm and precoMl < precoAme and precoMl != "0.00":
        #     precoMl.id = produto.id
        #     lista_produtos_atualizados.append(precoMl)
        # elif precoAm < precoMl and precoAm < precoAme and precoAm != "0.00":
        #     precoAm.id = produto.id
        #     lista_produtos_atualizados.append(precoAm)
        # elif precoAme !="0.00" :
        #     precoAme.id = produto.id
        #     lista_produtos_atualizados.append(precoAme)
    
    salvar_precos_encontrados(lista_produtos_atualizados, logging)

    lista_clientes = select_clientes(logging, getProdutos=True, getPrecos=True)
    for cliente in lista_clientes:
        carteiro.enviar_email(cliente.email, cliente.produtos)


if __name__ == "__main__":
    main()