from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Tarefa
from schemas import TarefaCreate, TarefaResponse

app = FastAPI(title="API de Tarefas", version="1.0.0")


# CREATE - Criar uma nova tarefa
@app.post("/tarefas", response_model=TarefaResponse, status_code=201)
def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    nova_tarefa = Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa


# READ ALL - Listar todas as tarefas
@app.get("/tarefas", response_model=list[TarefaResponse])
def listar_tarefas(db: Session = Depends(get_db)):
    tarefas = db.query(Tarefa).all()
    return tarefas


# READ ONE - Buscar uma tarefa por ID
@app.get("/tarefas/{tarefa_id}", response_model=TarefaResponse)
def buscar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


# UPDATE - Atualizar uma tarefa existente
@app.put("/tarefas/{tarefa_id}", response_model=TarefaResponse)
def atualizar_tarefa(tarefa_id: int, tarefa_data: TarefaCreate, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.titulo = tarefa_data.titulo
    tarefa.descricao = tarefa_data.descricao
    db.commit()
    db.refresh(tarefa)
    return tarefa


# DELETE - Deletar uma tarefa
@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
    return None
