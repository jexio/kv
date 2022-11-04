# Тестовое задание для компании KVINT

Бот доступен по ссылке https://t.me/KvintRabbitBot

# Supported types
* Text
* Photo

# How to run
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