from typing import Union
import uvicorn
from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.responses import JSONResponse
import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union


app = FastAPI()

pool_db: Pool

@app.on_event("startup")
async def create_database_pool():
    print('Создается пул подключений.')
    pool: Pool = await asyncpg.create_pool(host='host.docker.internal',
    port=5432,
    user='raulduke',
    password='kakacoarm',
    database='cars',
    min_size=6,
    max_size=6)
    global pool_db
    pool_db = pool


@app.on_event("shutdown")
async def destroy_database_pool():
        print('Уничтожается пул подключений.')
        pool: Pool = pool_db
        await pool.close()


@app.get("/")
async def main():
    return {"message": "Hello World"}


@app.get('/cars')
async def brands():
    connection: Pool = pool_db
    brand_query = 'SELECT * FROM cars;'
    results: List[Record] = await connection.fetch(brand_query)
    result_as_dict: List[Dict] = [dict(car) for car in results]
    return JSONResponse(result_as_dict)



@app.get('/cars/{vin}')
async def brands(vin: str):
    connection: Pool = pool_db
    brand_query = 'SELECT * FROM cars WHERE vin_nomer = $1;'
    results: List[Record] = await connection.fetch(brand_query, vin)
    if results:
        result_as_dict: List[Dict] = [dict(car) for car in results]
        return JSONResponse(result_as_dict)
    raise HTTPException(status_code=404, detail="Item not found")

@app.get('/checks_vin/{vin}')
async def check_vin(vin: str):
    connection: Pool = pool_db
    check_query = f"SELECT * FROM cars LEFT JOIN checks ON cars.car_id = checks.car WHERE cars.vin_nomer = '{vin}'"
    result: Record = await connection.fetchrow(check_query)
    if result:
        result_as_dict: Dict = dict(result)
        return JSONResponse(result_as_dict)
    raise HTTPException(status_code=404, detail="Item not found")

@app.get('/checks_gosnomer/{gosnomer}')
async def check_gosnomer(gosnomer: str):
    connection: Pool = pool_db
    check_query = f"SELECT * FROM cars LEFT JOIN checks ON cars.car_id = checks.car WHERE cars.gosnomer = '{gosnomer}'"
    result: Record = await connection.fetchrow(check_query)
    if result:
        result_as_dict: Dict = dict(result)
        return JSONResponse(result_as_dict)
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items")
def postdata(name=Form(), price=Form()):
    return {"name": name, "age": price}

@app.post("/upload-file/")
async def create_upload_file(name=Form(), price=Form(), uploaded_file: UploadFile = File(...)):
    file_location = f"files/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())
    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}

origins = [
    "https://testyoursite.ru"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(
               app,
               host="0.0.0.0",
               port=9002,
               ssl_keyfile="./key_cert.pem",
              ssl_certfile="./cert.pem"
               )
