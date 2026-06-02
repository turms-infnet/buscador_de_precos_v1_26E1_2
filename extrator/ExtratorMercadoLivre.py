from .ExtratorBase import ExtratorBase
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time

from model.Preco import Preco

class ExtratorMercadoLivre(ExtratorBase):
    def __init__(self, nome_produto, logging, seletors, headless=False):
        super().__init__(nome_produto, "https://lista.mercadolivre.com.br", logging, headless)
        self.seletors = seletors

    def buscar_url(self, url_final, wait):
        _driver = super().buscar_url(url_final, wait)

        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((self.seletors["select"]["type"], self.seletors["select"]["name"]))
        ).click()

        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((self.seletors["option"]["type"], self.seletors["option"]["name"]))
        ).click()

        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, wait))
        )
        time.sleep(2)

        return _driver

    def buscar_produto(self):
        termo_busca = self.nome_produto.replace(" ", "-")
        url_final = f"{self.url}/{termo_busca}"

        try:
            tag = "ui-search-result__wrapper"
            wait = f"div[class='{tag}']"

            driver = self.buscar_url(url_final, wait)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.find_all("div", class_=self.seletors["item"]) # "ui-search-result__wrapper"

            item = items[0]
            try:
                preco = item.find("span", class_=self.seletors["price"]).text #"andes-money-amount__fraction"
                preco = preco.replace(".", "")

                preco = float(f"{preco}.00")
            except Exception as e:
                preco = 0.00
                self.logging.error(f"Erro na precificação: {e}")

            link = item.find("a", class_=self.seletors["link"])["href"] #"poly-component__title"

            driver.close()

            return Preco(
                preco=preco,
                plataforma="MERCADO_LIVRE",
                link=link,
                id_produto=None
            )
        except Exception as e:
            self.logging.error(f"Erro ao buscar produto: {e}")
            return [None, "0.00", "MERCADO_LIVRE", None]