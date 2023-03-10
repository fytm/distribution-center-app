# distribution-center-app
A inventory management and payment system built using FastAPI
This app has two microservices, one for creating orders and payment, and one for handling the inventory.
The inventory microservice persists data using Redis cloud .
The payment microservice persists data using Redis cloud.
Inter service event driven communication is handled by Redis streams.

The original tutorial can be found at https://github.com/scalablescripts/fastapi-microservices