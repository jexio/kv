# Simple echo-bot

# Supported types
* Text
* Photo

# How to run
* Create the `.env` file based on the `.env.dev`
* Put your telegram bot token into the `.env` file.
* If you want to change the rabbitmq settings in the `.env` file, you should update them in `docker-compose.yaml` in the rmq section.
* Build base image
* Run containers

```yaml
docker build -f deploy/Dockerfile -t tg:latest .
```
```yaml
docker-compose -f deploy/docker-compose.yaml --project-directory . up
```

## Credits
* [aiogram][aiogram] aiogram is modern and fully asynchronous framework for Telegram Bot API.
* [aio-pika][aio-pika] aio-pika is a wrapper for the aiormq for asyncio and humans.
* [dependency injector][dependency-injector] Dependency injection framework for Python.

[aiogram]: https://aiogram.dev
[dependency-injector]: https://python-dependency-injector.ets-labs.org
[aio-pika]: https://aio-pika.readthedocs.io/en/latest/index.html