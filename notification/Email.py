from smtplib import SMTP
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .EmailFormatter import EmailFormatter


class Email:
    def __init__(self, email, password, logging):
        self.__email = email
        self.__password = password
        self.__logging = logging
        self.__servidor_smtp = "smtp.gmail.com"
        self.__porta = 587

    def enviar_email(self, cliente_email, lista_produtos=[]):
        data_atual = datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%Y")
        print(data_atual)

        mensagem = MIMEMultipart()
        mensagem["From"] = self.__email
        mensagem["To"] = cliente_email
        mensagem["Subject"] = f"Alerta de ofertas - Dia {data_formatada}"
        
        # formatar em html a lista de produtos em opferta
        corpo_html = EmailFormatter.formatar_lista_produtos(lista_produtos)
        mensagem.attach(MIMEText(corpo_html, "html"))

        try:
            servidor = SMTP(self.__servidor_smtp, self.__porta)
            servidor.starttls()
            servidor.login(self.__email, self.__password)
            servidor.sendmail(self.__email, cliente_email, mensagem.as_string())
            servidor.quit()

            self.__logging.info(
                f"E-mail enviado com sucesso para {cliente_email}"
            )

        except Exception as e:
            self.__logging.error(
                f"Um erro ocorreu ao tentar enviar o email para {cliente_email}. Erro: {e}"
            )