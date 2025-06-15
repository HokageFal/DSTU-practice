from fastapi import FastAPI
from api.crud.users import router as user_router
from api.crud.admin import router as admin_router
from api.crud.public import router as public_router
app = FastAPI()
app.include_router(user_router, )
app.include_router(admin_router, )
app.include_router(public_router, )
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

