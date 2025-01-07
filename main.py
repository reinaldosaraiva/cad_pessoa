from fastapi import FastAPI
from sqlmodel import SQLModel
from routers import pessoa
from database import engine 

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(pessoa.router)