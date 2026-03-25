# notification/EmailFormatter.py

class EmailFormatter:
    @staticmethod
    def formatar_lista_produtos(lista_produtos):
        html = "<h2>Seu Alerta de Preços Chegou! 🚀</h2>"

        for produto in lista_produtos:
            nome = produto["nome"]
            preco = str(produto["preco"]).replace(".", ",")
            loja = produto["loja"]
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