import asyncpg
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from asyncpg import Record
from asyncpg.pool import Pool
from typing import List, Dict
import ssl

sslcontext = ssl.create_default_context(
   cafile='./cert.pem')
sslcontext.load_cert_chain('./cert.pem',
                           './key_cert.pem')

routes = web.RouteTableDef()
DB_KEY = 'database'

app = web.Application()

@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
async def create_database_pool(app: Application):
    print('Создается пул подключений.')
    pool: Pool = await asyncpg.create_pool(host='localhost',
    port=5432,
    user='raulduke',
    password='kakacoarm',
    database='cars',
    min_size=6,
    max_size=6)
    app[DB_KEY] = pool
async def destroy_database_pool(app: Application):
    print('Уничтожается пул подключений.')
    pool: Pool = app[DB_KEY]
    await pool.close()
@routes.get('/cars')
async def brands(request: Request) -> Response:
    connection: Pool = request.app[DB_KEY]
    brand_query = 'SELECT * FROM cars;'
    results: List[Record] = await connection.fetch(brand_query)
    result_as_dict: List[Dict] = [dict(car) for car in results]
    return web.json_response(result_as_dict)



app.on_startup.append(create_database_pool)
app.on_cleanup.append(destroy_database_pool)
app.add_routes(routes)
web.run_app(app)