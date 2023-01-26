from redis_om import get_redis_connection
from dotenv import load_dotenv
import os

load_dotenv()

redis = get_redis_connection(
    host= os.getenv('DB_NAME'),
    port=os.getenv('DB_PORT'),
    password=os.getenv('DB_PASSWORD'),
    decode_responses=True
)