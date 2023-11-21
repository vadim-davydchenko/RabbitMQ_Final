import pika
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_order(ch, method, properties, body):
    order = json.loads(body)
    logger.info("Обработка заказа: %s", order)
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def process_inventory_update(ch, method, properties, body):
    update = json.loads(body)
    logger.info("Обновление инвентаря: %s", update)
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def process_catalog_update(ch, method, properties, body):
    update = json.loads(body)
    logger.info("Обновление каталога: %s", update)
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)

connected = False
while not connected:
    try:
        connection = pika.BlockingConnection(parameters)
        connected = True
    except pika.exceptions.AMQPConnectionError as e:
        logger.error("He удалось подключиться к RabbitMQ, ожидание... Причина: %s", e)
        time.sleep(10)

# Подписка на очереди
channel = connection.channel()

channel.queue_declare(queue='q_order', durable=True)
channel.queue_declare(queue='q_inventory', durable=True)
channel.queue_declare(queue='q_catalog', durable=True)

channel.basic_consume(queue='q_order', on_message_callback=process_order, auto_ack=False)
channel.basic_consume(queue='q_inventory', on_message_callback=process_inventory_update, auto_ack=False)
channel.basic_consume(queue='q_catalog', on_message_callback=process_catalog_update, auto_ack=False)

logger.info('Рабочий процесс запущен. Ожидание сообщений...')
channel.start_consuming()
