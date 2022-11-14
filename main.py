from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from todo.routers import tasks, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)

#app.mount("/static", StaticFiles(directory="static"), name="static")

#INDEXFILE = open('static/index.html','r').read()

#@app.get("/", response_class=HTMLResponse)
#async def index():
#    return INDEXFILE
