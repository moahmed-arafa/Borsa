import os
import urlparse

from redis import Redis
from rq import Worker, Queue, Connection
import redis

listen = ['default']

redis_url = os.getenv('REDIS_URL')

conn = redis.from_url(redis_url)
# redis_url = os.getenv('REDIS_URL')
#
# urlparse.uses_netloc.append('redis')
# url = urlparse.urlparse(redis_url)
# conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
