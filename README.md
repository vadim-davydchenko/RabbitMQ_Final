# RabbitMQ Final Project
This project is an example of an online store using RabbitMQ for asynchronous task processing in a distributed system.

**Main Components**

- **RabbitMQ**: Used to create and manage message queues and exchanges.
- **Web Service (Flask)**: Offers an interface to place orders and sends tasks to RabbitMQ for processing (orders, inventory, catalog updates).
- **Worker service**: Processes tasks from RabbitMQ queues (order processing, inventory and catalog updates).

**Functionality**

- Order queue (`q_order`): Orders from users go into this queue and are processed asynchronously by the worker-service.
- Inventory queue (`q_inventory`): Inventory update requests are sent to this queue and processed by the worker-service.
- Catalog queue (`q_catalog`): Requests to update the product catalog are sent to this queue and are also handled by the worker-service.
- Order exchanger (`x_order`): Used to route order messages to the order queue.
- Inventory exchanger (`x_inventory`): Used to route inventory messages to the inventory queue.
- Catalog Exchange (`x_catalog`): Used to route catalog messages to the catalog queue.

**Startup and Deployment**

The project is containerized using Docker and Docker Compose. All required services and their dependencies are defined in `docker-compose.yml`.

**Starting docker-compose**

`docker compose up --build`

RabbitMQ is available at `http://localhost:15672` (guest login and password).

The online store UI is available at `http://localhost:8080`
