from typing import Union
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



pool_db: Pool


app = FastAPI()

@app.on_event("startup")
async def create_database_pool():
    print('Создается пул подключений.')
    pool: Pool = await asyncpg.create_pool(host='localhost',
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

@app.get('/cars')
async def brands():
    connection: Pool = pool_db
    brand_query = 'SELECT * FROM cars;'
    results: List[Record] = await connection.fetch(brand_query)
    result_as_dict: List[Dict] = [dict(car) for car in results]
    return JSONResponse(result_as_dict)



if __name__ == '__main__':
    uvicorn.run(
               app,
               host="0.0.0.0",
               port=9000,
               ssl_keyfile="./key_cert.pem",
               ssl_certfile="./cert.pem"
               )
