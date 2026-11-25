from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from task_manager import list_tasks, create_task, get_task, complete_task, delete_task

app = FastAPI()

class TaskCreate(BaseModel):
    title: str

@app.get("/tasks")
def read_tasks():
    return list_tasks()

@app.post("/tasks",status_code=201)
def create_task_endpoint(task_data:TaskCreate):
    try:
        return create_task(task_data.title)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    try:
        return get_task(task_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

@app.patch("/tasks/{task_id}/complete")
def comeplete_task_endpoint(task_id: int):
    try:
        return complete_task(task_id)
    except ValueError as error:
        raise HTTPException(status_code=404,detail=str(error))

@app.delete("/tasks/{task_id}")
def delete_task_enpoint(task_id: int):
    try:
        return delete_task(task_id)
    except ValueError as error:
        raise HTTPException(status_code=404,detail=str(error))