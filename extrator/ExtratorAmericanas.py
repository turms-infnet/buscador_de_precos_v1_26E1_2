from .ExtratorBase import ExtratorBase
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
from utils import Money

class ExtratorAmericanas(ExtratorBase):
    def __init__(self, nome_produto, logging):
        super().__init__(nome_produto, "https://www.americanas.com.br", logging)

    def buscar_url(self, url_final, wait):
        _driver = super().buscar_url(url_final, wait)
        
        seletor = "div[class^='SortProducts_sortWrapper'] button"
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, seletor))
        ).click()

        seletor = "button[data-index='3']"
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, seletor))
        ).click()

        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, wait))
        )
        time.sleep(2)

        return _driver
        
    def buscar_produto(self):
        termo_busca = self.nome_produto.replace(" ", "+")
        url_final = f"{self.url}/s?q={termo_busca}"
        try: 
            tag = "ProductCard_productCard__MwY4X"
            wait = f"div[class='{tag}']"

            driver = self.buscar_url(url_final, wait)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.find_all("div", class_=tag)

            item = items[0]
            try:
                preco = item.find("p", class_="ProductCard_productPrice__XFEqu").text
                preco = Money.removeSpaceChar(preco)
            except Exception as e:
                preco = "0.00"
                self.logging.error(f"Erro na precificação: {e}")
                
            link = f"{driver.current_url}{item.find('a')['href']}"

            driver.close()

            return [None, preco, "AME", link]

        except Exception as e:
            self.logging.error(f"Erro ao buscar produto: {e}")
            return [None, "0.00", "AME", None]