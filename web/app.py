import logging
from flask import Flask, render_template, request, jsonify
import pika
import json
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# Connection to RabbitMQ
def connect_to_rabbitmq():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)

    while True:
        try:
            return pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("Failed to connect to RabbitMQ, pending... Reason: %s", e)
            time.sleep(10)

# Create a connection and channel in the global scope
connection = connect_to_rabbitmq()
channel = connection.channel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_order', methods=['POST'])
def submit_order():
    item_id = request.form['item_id']
    quantity = request.form['quantity']
    order = {'item_id': item_id, 'quantity': quantity}

    # Logic for sending a message to the q_order queue
    try:
        channel.exchange_declare(exchange='x_order', exchange_type='direct', durable=True)
        channel.basic_publish(exchange='x_order', routing_key='order', body=json.dumps(order))

        logger.info("The order has been successfully shipped to RabbitMQ: %s", order)
        return 'Заказ успешно размещен!'
    except Exception as e:
        logger.error("Order successfully placed: %s", e)
        return 'Error when placing an order', 500

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    item_id = request.form['item_id']
    quantity = request.form['quantity']
    update = {'item_id': item_id, 'quantity': quantity}

    # Logic for sending a message to the q_inventory queue
    try:
        channel.basic_publish(exchange='x_inventory', routing_key='inventory.update', body=json.dumps(update))
        logger.info("An inventory update message has been sent to RabbitMQ: %s", update)
        return 'The inventory has been successfully updated!'
    except Exception as e:
        logger.error("Error when sending  an inventory message: %s", e)
        return 'Error when updating inventory', 500

@app.route('/update_catalog', methods=['POST'])
def update_catalog():
    item_id = request.form['item_id']
    name = request.form['name']
    description = request.form.get('description', '')
    update = {'item_id': item_id, 'name': name, 'description': description}

    # Logic for sending a message to the q_catalog queue
    try:
        channel.basic_publish(exchange='x_catalog', routing_key='', body=json.dumps(update))
        logger.info("The message about updating the catalog has been sent to RabbitMQ: %s", update)
        return 'The catalog has been successfully updated!'
    except Exception as e:
        logger.error("Error when sending a message an catalog: %s", e)
        return 'Error during catalog update', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
