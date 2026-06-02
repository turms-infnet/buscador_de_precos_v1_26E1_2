from database.ormconnection import DeclarativeBase, Table, Column, ForeignKey

class Base(DeclarativeBase):
    __abstract__ = True

cliente_produto = Table(
    "cliente_produto",
    Base.metadata,
    Column("XID_CLIENTE", ForeignKey("cliente.ID_CLIENTE"), primary_key=True),
    Column("XID_PRODUTO", ForeignKey("produto.ID_PRODUTO"), primary_key=True),
)