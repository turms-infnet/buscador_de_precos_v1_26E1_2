from database.ormconnection import get_engine, get_session, select, update
from model.Base import Base, cliente_produto
from model.Produto import Produto
from model.Cliente import Cliente
from model.Preco import Preco

import random

def create_database():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

def populate_clientes():
    session = get_session()
    try:
        cls = [
            ["Tiago Silva", "tiagoluizrs@gmail.com"],
            ["Marcelo Sampaio", "marcelo.dsampaio@al.infnet.edu.br"],
            ["Arimar JR", "arimarjr@hotmail.com"],
            ["Suzana Silva", "suzana.silva@al.infnet.edu.br"],
            ["Viviane José", "viviene.jose@al.infnet.edu.br"],
        ]

        for c in cls:
            cliente = Cliente(
                nome=c[0],
                email=c[1]
            )
            session.add(cliente)
        
        session.commit()
    except Exception as e:
        session.rollback()
        print("[populate_clientes] >> Erro ao inserir clientes", e)
    finally:
        session.close()
    
def populate_produtos():
    session = get_session()
    try:
        prds = [
            Produto(nome="iPhone 15",),
            Produto(nome="Macbook Pro 2025",),
            Produto(nome="Macbook Air 2025",),
            Produto(nome="iPhone 16",),
            Produto(nome="iPhone 17",),
            Produto(nome="Samsung S25",)
        ]

        session.add_all(prds)
        session.commit()
    except Exception as e:
        session.rollback()
        print("[populate_clientes] >> Erro ao inserir clientes", e)
    finally:
        session.close()

def populate_clientes_produtos():
    session = get_session()
    try:
        clientes = session.scalars(select(Cliente)).all()

        for cliente in clientes:
            ids = []
            for r in range(3):
                id = random.randint(1, 6)
                if id not in ids:
                    ids.append(id)

            for id in ids:
                prod = session.get(Produto, id)
                cliente.produtos.append(prod)

        session.commit()
    except Exception as e:
        print(f"Erro: {e}")
        session.rollback()
    finally:
        session.close()

def salvar_precos_encontrados(precos, logging):
    session = get_session()
    try:
        stmt = (update(Preco).where(Preco.status == 1).value(status=0))
        session.execute(stmt)
        session.add_all(precos)
        session.commit()
    except Exception as e:
        logging.error(e)
        session.rollback()
    finally:
        session.close()

def select_clientes(logging):
    session = get_session()
    try:
        return session.scalars(select(Cliente)).all()
    except Exception as e:
        logging.error(e)
        return None
    finally:
        session.close()

def select_produtos(logging):
    session = get_session()
    try:
        return session.scalars(select(Produto)).all()
    except Exception as e:
        logging.error(e)
        return None
    finally:
        session.close()
    
if __name__ == "__main__":
    session = get_session()
    create_database()
    # populate_clientes(session)
    # populate_produtos(session)
    populate_clientes_produtos(session)
    session.close()

