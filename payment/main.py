import requests
import time
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from starlette.requests import Request

from database_config import redis

app= FastAPI()
app.add_middleware(
CORSMiddleware,
allow_origins =['http://localhost:3000/'],
allow_methods=['*'],
allow_headers=['*']
)



class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str #pending, completed, refunded

    class Meta:
        database = redis

@app.get("/")
def get(pk: str):
    return Order.get(pk)

@app.post("/")
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    req = requests.get('http://localhost:8000/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee =0.2 * product['price'],
        total = 1.2 * product['price'],
        quantity = body['quantity'],
        status='pending'
    )
    order.save()

    background_tasks.add_task(order_completed,order)
    return order

def order_completed(order: Order):
    time.sleep(5)
    order.status='completed'
    order.save()  
    redis.xadd('order_completed',order.dict(), '*')
       