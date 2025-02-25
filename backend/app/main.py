from fastapi import FastAPI
from app.routes import contracts
from app.config import setup_logging
app = FastAPI(title="Government Watch API")

app.include_router(contracts.router)

setup_logging()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Government Watch API"}