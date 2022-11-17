from fastapi import FastAPI
from pydantic import BaseModel
from meta_trader import initialize, login, get_account_info, send_order

initialized = initialize()
if not initialized:
    print("Erro ao inicializar.")
    quit()

class Credential(BaseModel):
    account: int
    password: str
    server: str

class OrderRequest(BaseModel):
    symbol: str

app = FastAPI()


@app.get("/")
async def root():
    return { 'message': 'Hello, this is a Metratrader API' }


@app.post("/login")
async def login(credential: Credential):
    logged = login(credential)
    if not logged:
        print("Erro ao logar.")
        quit()
    info = get_account_info()
    return info

@app.post("/order")
async def post_order(order_request: OrderRequest):
    info = send_order(order_request)
    if info is None:
        info = { 'message': 'Internal Server Error' }
    return info