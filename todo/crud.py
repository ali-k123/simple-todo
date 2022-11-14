from sqlalchemy.orm import Session
from .security import calculate_hash
from . import models, schemas


def get_user_by_username(db: Session, username : str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserIn):
    hashed_password = calculate_hash(user.password)
    db_user = models.User(name=user.name,username=user.username,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_tasks(db: Session, user_id : int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()


def create_user_task(db: Session, task: schemas.TaskIn, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def remove_user_task(db: Session, task_id: int, user_id: int):
    pass
