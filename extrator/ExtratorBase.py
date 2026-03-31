from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

class ExtratorBase(ABC):
    def __init__(self, nome_produto, url, logging):
        self.nome_produto = nome_produto
        self.url = url
        self.logging = logging

        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )

    def buscar_url(self, url_final, wait):
        time.sleep(random.uniform(2,5))

        self.driver.get(url_final)

        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, wait))
        )
        time.sleep(2)

        return self.driver

    @abstractmethod
    def buscar_produto(self):
        pass