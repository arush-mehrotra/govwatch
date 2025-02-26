from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import contracts
from app.config import setup_logging
import uvicorn
import os

app = FastAPI(title="Government Watch API")

# Get allowed origins from environment or use defaults
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://govwatch.xyz")
# Add additional domains as needed
allowed_origins = [
    FRONTEND_URL,
    "https://govwatch.example.com",
]

# Add CORS middleware with restricted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Restrict to needed methods
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(contracts.router)

setup_logging()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Government Watch API"}

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)
