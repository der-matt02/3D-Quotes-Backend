from fastapi import FastAPI
from core.database import initiate_database
from api import auth
from api import quotes

app = FastAPI()

# Cada vez que arranca el backend se conecta a mongo y registra los modelos
@app.on_event("startup")
async def startup_event():
    await initiate_database()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(quotes.router, prefix="/api/quotes", tags=["quotes"])
