import sqlite3

conn = sqlite3.connect("meu_banco.db")

def create_table():
    query = """
            CREATE TABLE IF NOT EXISTS produto (
                ID_PRODUTO INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT UNIQUE
            );
            
            CREATE TABLE IF NOT EXISTS cliente (
                ID_CLIENTE INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME TEXT,
                EMAIL TEXT UNIQUE
            );
            
            CREATE TABLE IF NOT EXISTS cliente_produto (
                XID_CLIENTE INTEGER,
                XID_PRODUTO INTEGER,
                FOREIGN KEY (XID_CLIENTE) REFERENCES cliente(ID_CLIENTE),
                FOREIGN KEY (XID_PRODUTO) REFERENCES produto(ID_PRODUTO)
            );

            CREATE TABLE IF NOT EXISTS preco (
                ID_PRECO INTEGER PRIMARY KEY AUTOINCREMENT,
                PLATAFORMA TEXT,
                LINK TEXT,
                XID_PRODUTO INTEGER,
                FOREIGN KEY (XID_PRODUTO) REFERENCES produto(ID_PRODUTO)
            );
    """
    conn.executescript(query)
    

def populate_clientes():
    try:
        cursor = conn.cursor()

        cursor.execute("INSERT INTO cliente (NOME, EMAIL) VALUES (?, ?)", ["Tiago Silva", "tiagoluizrs@gmail.com"])
        cursor.execute("INSERT INTO cliente (NOME, EMAIL) VALUES (?, ?)", ["Marcelo Sampaio", "marcelo.dsampaio@al.infnet.edu.br"])
        cursor.execute("INSERT INTO cliente (NOME, EMAIL) VALUES (?, ?)", ["Arimar JR", "arimarjr@hotmail.com"])
        cursor.execute("INSERT INTO cliente (NOME, EMAIL) VALUES (?, ?)", ["Suzana Silva", "suzana.silva@al.infnet.edu.br"])
        cursor.execute("INSERT INTO cliente (NOME, EMAIL) VALUES (?, ?)", ["Viviane José", "viviene.jose@al.infnet.edu.br"])

        conn.commit()
    except Exception as e:
        print("[populate_clientes] >> Erro ao inserir clientes", e)
        conn.rollback()
    
def populate_produtos():
    try:
        cursor = conn.cursor()

        cursor.executemany("INSERT INTO produto (NOME) VALUES (?)", [
            ("iPhone 15",),
            ("Macbook Pro 2025",),
            ("Macbook Air 2025",),
            ("iPhone 16",),
            ("iPhone 17",),
            ("Samsung S25",)
        ])
        
        conn.commit()
    except Exception as e:
        print("[populate_produtos] >> Erro ao inserir produtos", e)
        conn.rollback()

def populate_clientes_produtos():
    try:
        cursor = conn.cursor()

        cursor.executemany("INSERT INTO cliente_produto (XID_CLIENTE, XID_PRODUTO) VALUES (?, ?)", [
            (1, 1),
            (1, 2),
            (1, 3)
        ])
        cursor.executemany("INSERT INTO cliente_produto (XID_CLIENTE, XID_PRODUTO) VALUES (?, ?)", [
            (2, 1),
            (2, 3),
            (2, 4)
        ])
        cursor.executemany("INSERT INTO cliente_produto (XID_CLIENTE, XID_PRODUTO) VALUES (?, ?)", [
            (3, 1),
            (3, 4),
            (3, 6)
        ])
        cursor.executemany("INSERT INTO cliente_produto (XID_CLIENTE, XID_PRODUTO) VALUES (?, ?)", [
            (4, 2),
            (4, 5)
        ])
        cursor.executemany("INSERT INTO cliente_produto (XID_CLIENTE, XID_PRODUTO) VALUES (?, ?)", [
            (5, 4),
            (5, 5)
        ])
        
        conn.commit()
    except:
        conn.rollback()

if __name__ == "__main__":
    create_table()
    # populate_clientes()
    # populate_produtos()
    # populate_clientes_produtos()
    conn.close()
