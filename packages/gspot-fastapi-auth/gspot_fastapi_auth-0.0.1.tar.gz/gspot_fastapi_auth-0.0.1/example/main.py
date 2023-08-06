import uvicorn
from fastapi import FastAPI, Depends

from src.gspot_fastapi_auth import UserRedisAuth
from src.gspot_fastapi_auth.permissions import is_customer

app = FastAPI()


@app.get("/")
async def read_root(user=Depends(UserRedisAuth())):
    return user.to_dict()


@app.get("/customer/")
async def read_customer(user=Depends(is_customer)):
    return user.to_dict()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
