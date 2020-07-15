import pika
import datetime
import dbconnection
import redis

EXCHANGE = 'calc_logs'
tags = ['LOG', 'DEBUG', 'ERROR']


conn = dbconnection.DBConnection()
r = redis.Redis(host='localhost', port=7001)


def callback(ch, method, properties, body):
    time = datetime.datetime.now().__str__()
    tag = method.routing_key
    name = f'log:{time}'
    pipe = r.pipeline()
    pipe.hset(name, 'time', time)
    pipe.hset(name, 'tag', tag)
    pipe.hset(name, 'msg', body)
    pipe.execute()
    # conn.insert(datetime.datetime.now(), method.routing_key, body)


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    for tag in tags:
        channel.queue_bind(exchange=EXCHANGE,
                           queue=queue_name,
                           routing_key=tag)

    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback,
                          auto_ack=True)

    channel.start_consuming()
