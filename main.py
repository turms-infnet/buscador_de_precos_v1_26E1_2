import os
from dotenv import load_dotenv
import logging

from notification import Email

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
    lista_produtos = [
        {"nome": "iPhone 15", "loja": "ML", "link": "#", "preco": 3000.00},
        {"nome": "iPhone 17", "loja": "ML", "link": "#", "preco": 8000.00},
    ]

    email = Email(EMAIL, PASSWORD_APP, logging)
    email.enviar_email("tiago.silva@prof.infnet.edu.br", lista_produtos)


if __name__ == "__main__":
    main()