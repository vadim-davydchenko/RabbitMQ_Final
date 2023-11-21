import logging
from flask import Flask, render_template, request, jsonify
import pika
import json
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# Подключение к RabbitMQ
def connect_to_rabbitmq():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)

    while True:
        try:
            return pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError as e:
            logger.error("He удалось подключиться к RabbitMQ, ожидание... Причина: %s", e)
            time.sleep(10)

# Создание соединения и канал в глобальной области видимости
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

    # Логика отправки сообщения в очередь q_order
    try:
        channel.exchange_declare(exchange='x_order', exchange_type='direct', durable=True)
        channel.basic_publish(exchange='x_order', routing_key='order', body=json.dumps(order))

        logger.info("Заказ успешно отправлен в RabbitMQ: %s", order)
        return 'Заказ успешно размещен!'
    except Exception as e:
        logger.error("Ошибка при отправке заказа: %s", e)
        return 'Ошибка при размещении заказа', 500

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    item_id = request.form['item_id']
    quantity = request.form['quantity']
    update = {'item_id': item_id, 'quantity': quantity}

    # Логика отправки сообщения в очередь q_inventory
    try:
        channel.basic_publish(exchange='x_inventory', routing_key='inventory.update', body=json.dumps(update))
        logger.info("Сообщение ob обновлении инвентаря отправлено в RabbitMQ: %s", update)
        return 'Инвентарь успешно обновлен!'
    except Exception as e:
        logger.error("Ошибка при отправке сообщения ob инвентаре: %s", e)
        return 'Ошибка при обновлении инвентаря', 500

@app.route('/update_catalog', methods=['POST'])
def update_catalog():
    item_id = request.form['item_id']
    name = request.form['name']
    description = request.form.get('description', '')
    update = {'item_id': item_id, 'name': name, 'description': description}

    # Логика отправки сообщения в очередь q_catalog
    try:
        channel.basic_publish(exchange='x_catalog', routing_key='', body=json.dumps(update))
        logger.info("Сообщение ob обновлении каталога отправлено в RabbitMQ: %s", update)
        return 'Каталог успешно обновлен!'
    except Exception as e:
        logger.error("Ошибка при отправке сообщения ob каталоге: %s", e)
        return 'Ошибка при обновлении каталога', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
