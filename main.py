import os
from dotenv import load_dotenv
from extrator import ExtratorAmazon, ExtratorAmericanas, ExtratorMercadoLivre
import logging
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
    extratorMl = ExtratorMercadoLivre("Macbook Air", logging)
    produto = extratorMl.buscar_produto()

    # extratorAm = ExtratorAmazon("Iphone 15", logging)
    # produto = extratorAm.buscar_produto()

    # extratorAm = ExtratorAmericanas("Iphone 15", logging)
    # produto = extratorAm.buscar_produto()
    print(produto)

if __name__ == "__main__":
    main()