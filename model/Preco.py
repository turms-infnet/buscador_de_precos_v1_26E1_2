from datetime import datetime
from typing import List

from .Base import Base, cliente_produto
from database.ormconnection import mapped_column, String, ForeignKey, Mapped, Float, DateTime, func, relationship

class Preco(Base):
    __tablename__ = "preco"

    id: Mapped[int] = mapped_column(primary_key=True, name='ID_PRECO')
    preco: Mapped[float] = mapped_column(Float, name="PRECO")
    plataforma: Mapped[str] = mapped_column(String(20), nullable=False, name="PLATAFORMA")
    link: Mapped[str] = mapped_column(String(255), nullable=False, name="LINK")
    id_produto: Mapped[int] = mapped_column(ForeignKey("produto.ID_PRODUTO"), name="XID_PRODUTO")
    status: Mapped[int] = mapped_column(default=1, name="STATUS")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), name="CREATED_AT")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), name="UPDATED_AT")
    produto: Mapped[List["Produto"]] = relationship(
        back_populates="precos"
    )