from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import contracts
from app.config import setup_logging
import uvicorn

app = FastAPI(title="Government Watch API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contracts.router)

setup_logging()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Government Watch API"}

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)
