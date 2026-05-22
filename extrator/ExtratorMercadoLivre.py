from .ExtratorBase import ExtratorBase
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time

class ExtratorMercadoLivre(ExtratorBase):
    def __init__(self, nome_produto, logging):
        super().__init__(nome_produto, "https://lista.mercadolivre.com.br", logging)

    def buscar_url(self, url_final, wait):
        _driver = super().buscar_url(url_final, wait)

        # seletor = "#_R_5clcj6e_-trigger"
        # WebDriverWait(self.driver, 30).until(
        #     expected_conditions.presence_of_element_located((By.ID, seletor))
        # ).click()

        # seletor = "#_R_5clcj6e_-menu-list-option-price_asc"
        # WebDriverWait(self.driver, 30).until(
        #     expected_conditions.presence_of_element_located((By.ID, seletor))
        # ).click()

        # WebDriverWait(self.driver, 30).until(
        #     expected_conditions.presence_of_element_located((By.CSS_SELECTOR, wait))
        # )
        # time.sleep(2)

        return _driver

        # //input[@data-testid='Minimum-INTERNAL_MEMORY' and @name='Minimum']

    def buscar_produto(self):
        termo_busca = self.nome_produto.replace(" ", "-")
        url_final = f"{self.url}/{termo_busca}"

        try:
            tag = "ui-search-result__wrapper"
            wait = f"div[class='{tag}']"

            driver = self.buscar_url(url_final, wait)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.find_all("div", class_="ui-search-result__wrapper")

            item = items[0]
            try:
                preco = item.find("span", class_="andes-money-amount__fraction").text
                preco = preco.replace(".", "")

                centavos = item.find("span", class_="andes-money-amount__cents").text
                
                if centavos:
                    preco = f"{preco}.{centavos}"
                else:
                    preco = f"{preco}.00"
            except Exception as e:
                preco = "0.00"
                self.logging.error(f"Erro na precificação: {e}")

            link = item.find("a", class_="poly-component__title")["href"]

            driver.close()

            return [None, preco, "MERCADO_LIVRE", link]
        except Exception as e:
            self.logging.error(f"Erro ao buscar produto: {e}")
            return [None, "0.00", "MERCADO_LIVRE", None]