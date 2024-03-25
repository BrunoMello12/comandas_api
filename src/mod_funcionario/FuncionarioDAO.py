from fastapi import APIRouter
from mod_funcionario.Funcionario import Funcionario
router = APIRouter()
# Criar as rotas/endpoints: GET, POST, PUT, DELETE
@router.get("/funcionario/", tags=["Funcionário"])
def get_funcionario():
  return {"msg": "get todos executado"}, 200
@router.get("/funcionario/{id}", tags=["Funcionário"])
def get_funcionario(id: int):
  return {"msg": "get um executado"}, 200
@router.post("/funcionario/", tags=["Funcionário"])
def post_funcionario(f: Funcionario):
  return {"msg": "post executado", "nome": f.nome, "cpf": f.cpf, "telefone": f.telefone }, 200
@router.put("/funcionario/{id}", tags=["Funcionário"])
def put_funcionario(id: int, f: Funcionario):
  return {"msg": "put executado", "id": id, "nome": f.nome, "cpf": f.cpf, "telefone": f.telefone}, 201
@router.delete("/funcionario/{id}", tags=["Funcionário"])
def delete_funcionario(id: int):
  return {"msg": "delete executado"}, 201