from typing import List
from datetime import datetime

from .Base import Base, cliente_produto
from database.ormconnection import mapped_column, String, relationship, Mapped, Float, DateTime, func

class Produto(Base):
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(primary_key=True, name='ID_PRODUTO')
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, name="NOME")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), name="CREATED_AT")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), name="UPDATED_AT")
    clientes: Mapped[List["Cliente"]] = relationship(
        secondary=cliente_produto, back_populates="produtos"
    )
    precos: Mapped[List["Preco"]] = relationship(
        back_populates="produto"
    )

    def __repr__(self):
        return f"<Produto: {self.nome} - {self.id}>"