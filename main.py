from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.pessoa.router import router as pessoa_router

app = FastAPI(
    title="Cadastro de Pessoas API",
    description="API para gerenciamento de cadastro de pessoas",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo os routers
app.include_router(pessoa_router)

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API de Cadastro de Pessoas",
        "docs": "/docs",
        "redoc": "/redoc"
    }