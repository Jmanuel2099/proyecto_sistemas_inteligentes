from fastapi import FastAPI
from preprocessing_service.router import preprocessing_router
from training_service.presentation.router import training_router


app = FastAPI()

app.include_router(preprocessing_router.router)
app.include_router(training_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome"}