import asyncio
import logging
import os

from dotenv import load_dotenv
from yarl import URL

from kv.mq.rpc import Consumer
from kv.mq.scheme import RabbitConnectionSettings


if __name__ == '__main__':
    load_dotenv()
    url = str(URL.build(
        scheme="amqp",
        host=os.getenv("rabbit_host"),
        port=os.getenv("rabbit_port"),
        user=os.getenv("rabbit_user"),
        password=os.getenv("rabbit_password"),
        path=os.getenv("rabbit_vhost"),
    ))
    settings = RabbitConnectionSettings(url=url)
    consumer = Consumer(settings)
    logger = logging.getLogger(__name__)
    logger.debug("The Consumer has been launched.")
    asyncio.run(consumer.start())
