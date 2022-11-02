from fastapi import FastAPI
from pydantic import BaseModel
from meta_trader import initialize, login, get_account_info

initialized = initialize()
if not initialized:
    print("Erro ao inicializar.")
    quit()

class Credential(BaseModel):
    account: int
    password: str
    server: str

app = FastAPI()


@app.get("/")
async def root():
    logged = login()
    if not logged:
        print("Erro ao logar.")
        quit()
    info = get_account_info()
    return info


@app.post("/")
async def login(credential: Credential):
    logged = login(credential)
    if not logged:
        print("Erro ao logar.")
        quit()
    info = get_account_info()
    return info