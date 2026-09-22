from typing import Dict, List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=1)
    completed: bool = False


class Todo(TodoCreate):
    id: int


app = FastAPI(title="Todo API")

_todos: Dict[int, Todo] = {}
_next_id = 1


@app.get("/todos", response_model=List[Todo])
def list_todos() -> List[Todo]:
    return list(_todos.values())


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate) -> Todo:
    global _next_id

    created = Todo(id=_next_id, title=todo.title, completed=todo.completed)
    _todos[_next_id] = created
    _next_id += 1
    return created


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    todo = _todos.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate) -> Todo:
    if todo_id not in _todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    updated = Todo(id=todo_id, title=todo.title, completed=todo.completed)
    _todos[todo_id] = updated
    return updated


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int) -> None:
    if todo_id not in _todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    del _todos[todo_id]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
