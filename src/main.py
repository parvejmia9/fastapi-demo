from fastapi import FastAPI
from src.models import Base
from src.routes.user_routes import router as userRouter
from src.routes.room_routes import router as roomRouter
from src.routes.message_routes import router as messageRouter

app = FastAPI()
app.include_router(userRouter)
app.include_router(roomRouter)
app.include_router(messageRouter)

@app.get("/",)
def read_root():
    return {"Hello": "World"}

