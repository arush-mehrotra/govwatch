from fastapi import FastAPI
from app.routes import contracts

app = FastAPI(title="Government Watch API")

app.include_router(contracts.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Government Watch API"}