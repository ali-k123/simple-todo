from pydantic import BaseModel, Field, EmailStr

class Task(BaseModel):
    id : int
    title : str = Field(min_length = 1, max_length = 16)
    description : str | None =  Field(default = None, max_length = 256)
    owner_id : int
    
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    name : str
    username : str
    tasks: list[Task] = []

    class Config:
        orm_mode = True

class TaskIn(BaseModel):
    title : str = Field(min_length = 1, max_length = 16)
    description : str | None = Field(default = None, max_length = 256)

class UserIn(BaseModel):
    name : str = Field(min_length = 1, max_length = 32)
    username : str
    password : str = Field(min_length = 8, max_length = 32)
    password2 : str = Field(min_length = 8, max_length = 32)

#csvjsm12@proton.me

#f1nx5@jbu3l

