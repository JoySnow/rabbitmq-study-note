#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='logs',
                        type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange='logs',
                    routing_key='',
                    body=message)

print (" [x] Sent %r" % message)

connection.close()

# code source:
#     https://www.rabbitmq.com/tutorials/tutorial-three-python.html
