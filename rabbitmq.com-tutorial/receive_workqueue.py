#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='task_queue_', durable=True)

def callback(ch, method, properties, body):
    print (" [x] Recived %r" % body)
    time.sleep(body.count(b'.'))
    print (" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                    queue='task_queue_',
                    no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# code source:
#     https://www.rabbitmq.com/tutorials/tutorial-two-python.html
