import pika
from rmworker.config import RM_Settings

rm_user = RM_Settings.RM_USER
rm_password = RM_Settings.RM_PASSWORD
rm_host = RM_Settings.RM_HOST
rm_port = RM_Settings.RM_PORT

# Параметры подключения
connection_params = pika.ConnectionParameters(
    host=rm_host,  # Замените на адрес вашего RabbitMQ сервера
    port=rm_port,  # Порт по умолчанию для RabbitMQ
    virtual_host="/",  # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username=rm_user,  # Имя пользователя по умолчанию
        password=rm_password,  # Пароль по умолчанию
    ),
    heartbeat=30,
    blocked_connection_timeout=2,
)

# Имя очереди
queue_name = "prediction_queue"
