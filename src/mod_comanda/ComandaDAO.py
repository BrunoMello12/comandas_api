from fastapi import APIRouter
from mod_comanda.Comanda import Comanda, ComandaProdutos
# import da persistência
import db
from mod_comanda.ComandaModel import ComandaDB, ComandaProdutoDB
from mod_produto.ProdutoModel import ProdutoDB
from mod_funcionario.FuncionarioModel import FuncionarioDB
from mod_cliente.ClienteModel import ClienteDB

# import da segurança
from typing import Annotated
from fastapi import Depends
from security import get_current_active_user, User

#router = APIRouter()
# dependências de forma global
router = APIRouter(dependencies=[Depends(get_current_active_user)])

#BRUNO VINICIUS MELLO

@router.get("/comanda/{id_comanda}", tags=["Comanda"])
def get_comanda(id_comanda: int):
    try:
        session: Session = SessionLocal()
        aux_dados = session.query(ComandaDB, FuncionarioDB, ClienteDB)\
            .select_from(ComandaDB)\
            .join(FuncionarioDB, FuncionarioDB.id_funcionario == ComandaDB.funcionario_id, isouter=False)\
            .join(ClienteDB, ClienteDB.id_cliente == ComandaDB.cliente_id, isouter=True)\
            .filter(ComandaDB.id_comanda == id_comanda)\
            .order_by(ComandaDB.id_comanda)\
            .all()

        dados = []
        for row in aux_dados:
            dados.append({'comanda': row[0], 'funcionario': row[1], 'cliente': row[2]})
        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/comanda/status/{status}", tags=["Comanda"])
def get_comanda(status: int):
    try:
        session: Session = SessionLocal()
        aux_dados = session.query(ComandaDB, FuncionarioDB, ClienteDB)\
            .select_from(ComandaDB)\
            .join(FuncionarioDB, FuncionarioDB.id_funcionario == ComandaDB.funcionario_id, isouter=False)\
            .join(ClienteDB, ClienteDB.id_cliente == ComandaDB.cliente_id, isouter=True)\
            .filter(ComandaDB.status == status)\
            .order_by(ComandaDB.id_comanda)\
            .all()

        dados = []
        for row in aux_dados:
            dados.append({'comanda': row[0], 'funcionario': row[1], 'cliente': row[2]})
        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/comanda", tags=["Comanda"])
def post_comanda(corpo: Comanda):
    try:
        session: Session = SessionLocal()
        dados = session.query(ComandaDB).filter(ComandaDB.comanda == corpo.comanda).filter(ComandaDB.status == 0).all()
        if len(dados) > 0:
            return dados, 300
        else:
            nova_comanda = ComandaDB(None, corpo.comanda, corpo.data_hora, corpo.status, corpo.funcionario_id, corpo.cliente_id)
            session.add(nova_comanda)
            session.commit()
            return {"id": nova_comanda.id_comanda}, 200

    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/comanda", tags=["Comanda"])
def put_comanda(corpo: Comanda):
    try:
        session: Session = SessionLocal()
        comanda_atual = session.query(ComandaDB).filter(ComandaDB.id_comanda == corpo.id_comanda).one()
        comanda_atual.comanda = corpo.comanda
        comanda_atual.data_hora = corpo.data_hora
        comanda_atual.status = corpo.status
        comanda_atual.funcionario_id = corpo.funcionario_id
        comanda_atual.cliente_id = corpo.cliente_id
        session.add(comanda_atual)
        session.commit()
        return {"id": comanda_atual.id_comanda}, 200

    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.post("/comanda/item", tags=["Comanda"])
def post_comanda_item(corpo: ComandaProdutos):
    try:
        session: Session = SessionLocal()
        novo_item_comanda = ComandaProdutoDB(None, corpo.comanda_id, corpo.produto_id, corpo.funcionario_id, corpo.quantidade, corpo.valor_unitario)
        session.add(novo_item_comanda)
        session.commit()
        return {"id": novo_item_comanda.id_comanda_produto}, 200

    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/comanda/{comanda_id}/item", tags=["Comanda"])
def get_comanda_item(comanda_id: int):
    try:
        session: Session = SessionLocal()
        aux_dados = session.query(ComandaProdutoDB, FuncionarioDB, ProdutoDB)\
            .select_from(ComandaProdutoDB)\
            .join(FuncionarioDB, FuncionarioDB.id_funcionario == ComandaProdutoDB.funcionario_id, isouter=False)\
            .join(ProdutoDB, ProdutoDB.id_produto == ComandaProdutoDB.produto_id, isouter=False)\
            .filter(ComandaProdutoDB.comanda_id == comanda_id)\
            .order_by(ComandaProdutoDB.quantidade)\
            .all()

        dados = []
        for row in aux_dados:
            dados.append({'comanda_produto': row[0], 'funcionario': row[1], 'produto': row[2]})
        return dados, 200

    except Exception as e:
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.put("/comanda/item", tags=["Comanda"])
def put_comanda_item(corpo: ComandaProdutos):
    try:
        session: Session = SessionLocal()
        item_atual = session.query(ComandaProdutoDB).filter(ComandaProdutoDB.id_comanda_produto == corpo.id_comanda_produto).one()

        if corpo.quantidade == 0:
            session.delete(item_atual)
        else:
            item_atual.funcionario_id = corpo.funcionario_id
            item_atual.quantidade = corpo.quantidade
            item_atual.valor_unitario = corpo.valor_unitario

        session.commit()
        return {"id": item_atual.id_comanda_produto}, 200

    except Exception as e:
        session.rollback()
        return {"erro": str(e)}, 400
    finally:
        session.close()

@router.get("/comandas/{comanda_id}", tags=["Comanda"])
def get_comanda_total(comanda_id: int):
    try:
        session: Session = SessionLocal()
        total = session.query(func.sum(ComandaProdutoDB.quantidade * ComandaProdutoDB.valor_unitario).label("Total:"))\
            .filter(ComandaProdutoDB.comanda_id == comanda_id)\
            .scalar()

        return {"total_comanda": total}, 200

    except Exception as e:
      return {"erro": str(e)}, 400
    finally:
      session.close()