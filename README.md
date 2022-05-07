# Order service

This service is designed to:
- provide simple ordering operations
- CRUD for Item entities
- CRUD for Order entities

## Item endpoints
- GET /items/ - Return info about all items (products) that server contains
- GET /items/{item_id}/ - Returns info about particular item
- POST /items/{item_id}/ - Add new item to server
- PUT /items/{item_id}/ - Update fields for particular item
- DELETE /items/{item_id}/ - Delete existed item

## Order endpoints
- GET /orders/ - Return info about all orders that server contains
- GET /orders/{order_id}/ - Returns info about particular order
- POST /orders/{order_id}/ - Add new order to server
- PUT /orders/{order_id}/ - Update fields for particular order
- DELETE /orders/{order_id}/ - Delete existed order

## Start service
To start service using Docker:
1. Specify fields that .env.example contains
2. Change file name .env.example to .env
3. Use command: `docker-compose up --build`

## Using OpenAPI (Swagger)

Open in browser [localhost:8000/docs](localhost:8000/docs)
