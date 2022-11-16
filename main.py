from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from todo.routers import tasks, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)
