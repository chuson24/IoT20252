import json
import pika

AMQP_URL = "amqps://riisiskm:a6OGRyh-7mk4KEoKlO3uXoRNjThxFZe3@gerbil.rmq.cloudamqp.com/riisiskm"
QUEUE_NAME = "sensor_queue"

def on_message(channel, method, properties, body: bytes):
    try:
        text = body.decode("utf-8")
        data = json.loads(text)

        device = data.get("DeviceName", "Unknown")
        temp = data.get("temperature", None)
        hum = data.get("humidity", None)

        print("----- [Consumer] Received -----")
        print(f"Raw JSON: {text}")
        print(f"DeviceName: {device}")
        print(f"temperature: {temp}")
        print(f"humidity: {hum}")
        print("------------------------------")

        channel.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[Consumer] Error: {e}")
        # Không ack để message có thể được gửi lại (tuỳ chọn)
        # channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    params = pika.URLParameters(AMQP_URL)
    params.heartbeat = 30
    params.blocked_connection_timeout = 30

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message, auto_ack=False)

    print("[Consumer] Waiting for messages... CTRL+C to exit.")
    channel.start_consuming()

if __name__ == "__main__":
    main()

