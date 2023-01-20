from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app= FastAPI()
app.add_middleware(
CORSMiddleware,
allow_origins =['http://localhost:3000/'],
allow_methods=['*'],
allow_headers=['*']
)

load_dotenv()

redis = get_redis_connection(
    host= os.getenv('DB_NAME'),
    port=os.getenv('DB_PORT'),
    password=os.getenv('DB_PASSWORD'),
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis    

@app.get("/")
def allProducts():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)    

    return{
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post("/")
def createProduct(product: Product):
    return product.save()

@app.get("/{pk}")
def getProduct(pk: str):
    return Product.get(pk)

@app.delete("/{pk}")
def deleteProduct(pk: str):
    return Product.delete(pk)    