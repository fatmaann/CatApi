from fastapi import FastAPI
from api.kitten_router import router as kittens_router
from api.breed_router import router as breeds_router
from db.database import create_tables

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_tables()


app.include_router(kittens_router)
app.include_router(breeds_router)
