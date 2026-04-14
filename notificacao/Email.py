from smtplib import SMTP
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    def __init__(self, email, password, logging):
        self.__email = email
        self.__password = password
        self.__logging = logging
        self.__servidor_smtp = "smtp.gmail.com"
        self.__porta = 587
    
    def formatar_html(self, lista_produtos):
        html = "<h2>Seu Alerta de Preços Chegou! 🚀</h2>"

        for produto in lista_produtos:
            nome = produto["nome"]
            preco = str(produto["preco"]).replace(".", ",")

            if produto["plataforma"] == "MERCADO_LIVRE":
                loja = "Mercado Livre"
            elif produto["plataforma"] == "AM":
                loja = "Amazon"
            else:
                loja = "Americanas"
                
            link = produto["link"]

            html += f"""
                <div style="margin-bottom:20px;border-bottom:1px solid #ccc;padding-bottom:10px">
                    <p><strong>Buscado:</strong> {nome}</p>
                    <p><strong>Encontrado:</strong> {loja}</p>
                    <p><strong>Preço:</strong> <span style="color: green; font-size: 1.2em;">R$ {preco}</span></p>
                    <a href="{link}" style="background-color:#007bff;color:white;padding:10px 15px;text-decoration:none;border-radius:5px">Acessar oferta</a>
                </div>
            """

        return html


    def enviar_email(self, cliente_email, lista_produtos=[]):
        data_atual = datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%Y")
        print(data_atual)

        mensagem = MIMEMultipart()
        mensagem["From"] = self.__email
        mensagem["To"] = cliente_email
        mensagem["Subject"] = f"Alerta de ofertas - Dia {data_formatada}"
        
        corpo_html = self.formatar_html(lista_produtos)
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

