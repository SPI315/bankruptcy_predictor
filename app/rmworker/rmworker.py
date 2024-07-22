import pika
import json
import pandas as pd

from services.ml import OperModel
from database.database import SessionLocal

session = SessionLocal()


# Функция, которая будет вызвана при получении сообщения
def callback(ch, method, properties, body):
    model = OperModel()
    message = json.loads(body)
    user_id = next(iter(message.keys()))
    data_dict = {key: [value] for key, value in message[user_id].items()}
    data = pd.DataFrame(data_dict)
    column_names = [
        "X1",
        "X2",
        "X3",
        "X5",
        "X6",
        "X7",
        "X10",
        "X11",
        "X12",
        "X13",
        "X14",
        "X15",
        "X17",
    ]
    data.columns = column_names
    response = model.response(data)

    ch.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=json.dumps(response),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def worker_run(connection_params, queue_name):
    # Установка соединения
    connection = pika.BlockingConnection(connection_params)
    # Создание канала
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    # Потребитель будет получать 1 сообщение за раз, прежде, чем получить следующее
    channel.basic_qos(prefetch_count=1)
    # Подписка на очередь и установка обработчика сообщений
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("Waiting for messages. To exit, press Ctrl+C")
    channel.start_consuming()
