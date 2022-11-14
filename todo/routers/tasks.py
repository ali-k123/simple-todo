from fastapi import APIRouter, Body, Depends
from fastapi import HTTPException, status, Form
from ..schemas import User, TaskIn, Task
from ..dependencies import get_user
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import get_tasks,create_user_task

router = APIRouter()

@router.get("/get_tasks",response_model=list[Task])
async def get_lists(user: User = Depends(get_user),db : Session = Depends(get_db)):
    x = get_tasks(db, user.id)
    print(x)
    return x

@router.post("/add_task")
async def add_task(task : TaskIn, user : User = Depends(get_user),db : Session = Depends(get_db)):
    return create_user_task(db, task, user.id)

