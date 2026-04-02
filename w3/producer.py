import json
import time
import pika

AMQP_URL = "amqps://riisiskm:a6OGRyh-7mk4KEoKlO3uXoRNjThxFZe3@gerbil.rmq.cloudamqp.com/riisiskm"
QUEUE_NAME = "sensor_queue"

def main():
    params = pika.URLParameters(AMQP_URL)

    # CloudAMQP dùng TLS (amqps) -> thường cần set heartbeat/blocked_timeout để ổn định
    params.heartbeat = 30
    params.blocked_connection_timeout = 30

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Cloud queue declare
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    device_name = "Producer-1"

    for i in range(10):
        payload = {
            "DeviceName": device_name,
            "temperature": 30 + (i % 5),
            "humidity": 60 + (i % 10)
        }

        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=body,
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2
            )
        )

        print(f"[Producer] Sent: {payload}")
        time.sleep(1)

    connection.close()
    print("[Producer] Done.")

if __name__ == "__main__":
    main()
