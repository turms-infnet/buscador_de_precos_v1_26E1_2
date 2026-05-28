from config.conn import get_engine
from model.Base import Base, cliente_produto
from model.Produto import Produto
from model.Cliente import Cliente
from model.Preco import Preco

def create_database():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    create_database()