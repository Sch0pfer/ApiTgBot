from fastapi import FastAPI
from users.views import router as user_router
app = FastAPI()
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Hello World!"}