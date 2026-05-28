from typing import List
from datetime import datetime

from .Base import Base, cliente_produto
from config.conn import mapped_column, String, relationship, Mapped, Float, DateTime, func

class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True, name='ID_CLIENTE')
    nome: Mapped[str] = mapped_column(String(70), nullable=False, name="NOME")
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, name="EMAIL")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), name="CREATED_AT")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), name="UPDATED_AT")
    produtos: Mapped[List["Produto"]] = relationship(
        secondary=cliente_produto, back_populates="clientes"
    )