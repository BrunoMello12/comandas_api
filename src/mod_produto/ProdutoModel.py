import db
from sqlalchemy import Column, VARCHAR, CHAR, Integer
from sqlalchemy.types import BLOB
from sqlalchemy.types import Float
# ORM

class ProdutoDB(db.Base):
  __tablename__ = 'tb_produto'

  id_produto = Column(Integer, primary_key=True, autoincrement=True, index=True)
  nome = Column(VARCHAR(100), nullable=False)
  descricao = Column(VARCHAR(200), nullable=False)
  foto = Column(BLOB, nullable=False)
  valor_unitario = Column(Float, nullable=False)

  def __init__(self, id_produto, nome, descricao, foto, valor_unitario):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.foto = foto
        self.valor_unitario = valor_unitario