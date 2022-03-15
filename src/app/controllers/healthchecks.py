from fastapi import APIRouter

app = APIRouter()

@app.get("")
async def healthcheck():
    return {"message": "alive"}