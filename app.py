from fastapi import FastAPI
from api.kitten_router import router as kittens_router
from api.breed_router import router as breeds_router

app = FastAPI()

app.include_router(kittens_router)
app.include_router(breeds_router)
