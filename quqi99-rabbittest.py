#coding:utf-8
import sys
from amqplib import client_0_8 as amqp
if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        ispublisher = '0'
        print "Then pls run 'rabbittest 1' to sent message."
    else:
        ispublisher = sys.argv[1]
    conn = amqp.Connection(host="localhost:25672 ", userid="guest", password="password", virtual_host="/", insist=False)
    # 每个channel都被分配了一个整数标识
    chan = conn.channel()
    # 创建一个队列，它是durable的（重启后会重新建立）a
    # 消费者断开时不会自动删除（auto_delte=False)
    chan.queue_declare(queue="queue1", durable=True, exclusive=False, auto_delete=False)
    # 创建交换机，参数意思和上面的队列是一样的，还有一个type类型：fanout, direct, topic
    chan.exchange_declare(exchange="switch1", type="direct",
                          durable=True, auto_delete=False,)
    # 绑定交换机和队列
    chan.queue_bind(queue="queue1", exchange="switch1", routing_key="key1")
    if (ispublisher == '1'):
        # 生产者
        msg = amqp.Message("Test message!")
        msg.properties["delivery_mode"] = 2
        chan.basic_publish(msg, exchange="switch1", routing_key="key1")
    else:
        # 主动从队列拉消息
        msg = chan.basic_get("queue1")
        print msg.body
        chan.basic_ack(msg.delivery_tag)
        # 消息来了通知回调
        # 如果no_ack=True可以使用chan.basic_ack()人工确认，使用delivery_tag参数
        def recv_callback(msg):
            print 'Received: ' + msg.body
        chan.basic_consume(queue='queue1', no_ack=False,
                           callback=recv_callback, consumer_tag="testtag")
        # chan.basic_cancel("testtag") # 取消回调函数
        while True:
            chan.wait()  # 等待在队列上，直到下一个消息到达队列。
    chan.close()
    conn.close()
