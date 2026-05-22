import sqlite3

def open_connection():
    try:
        conn = sqlite3.connect("meu_banco.db")
        return conn
    except Exception as e:
        print("[open_connection] >> Erro ao abrir conexão com o banco de dados", e)
        return None

def create_table(conn):
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
                STATUS INTEGER DEFAULT 1,
                FOREIGN KEY (XID_PRODUTO) REFERENCES produto(ID_PRODUTO)
            );
    """
    conn.executescript(query)
    
def populate_clientes(conn):
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
    finally:
        cursor.close()
    
def populate_produtos(conn):
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
    finally:
        cursor.close()

def populate_clientes_produtos(conn):
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
    finally:
        cursor.close()

def salvar_precos_encontrados(conn, data, logging):
    try:
        cursor = conn.cursor()

        cursor.executemany("INSERT INTO preco (PLATAFORMA, LINK, XID_PRODUTO, STATUS) VALUES (?, ?, ?, ?)", data)
        conn.commit()
    except:
        conn.rollback()
    finally:
        cursor.close()

def select_cliente_produtos(conn, id, logging, isDict=False):
    try:
        if isDict:
            conn.row_factory = sqlite3.Row
        else:
            conn.row_factory = None

        rows = conn.execute("SELECT XID_PRODUTO FROM cliente_produto WHERE XID_CLIENTE = ?;", [id])
        list_ids = rows.fetchall()

        ids = []
        for _id in list_ids:
            ids.append(_id[0])

        return ids
    
    except Exception as e:
        logging.error(e)
        return None

def select_clientes(conn, logging, isDict=False):
    try:
        if isDict:
            conn.row_factory = sqlite3.Row
        else:
            conn.row_factory = None

        rows = conn.execute("SELECT * FROM cliente;")
        return rows.fetchall()
    except Exception as e:
        logging.error(e)
        return None

def select_produtos(conn, logging, isDict=False):
    try:
        if isDict:
            conn.row_factory = sqlite3.Row
        else:
            conn.row_factory = None

        rows = conn.execute("SELECT * FROM produto;")
        return rows.fetchall()
    except Exception as e:
        logging.error(e)
        return None
    
if __name__ == "__main__":
    conn = open_connection()
    create_table(conn)
    # populate_clientes(conn)
    # populate_produtos(conn)
    # populate_clientes_produtos(conn)
    conn.close()
