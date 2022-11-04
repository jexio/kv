from ssl import SSLContext
from typing import Dict, Optional, Union

from aio_pika.abc import SSLOptions
from pydantic import BaseSettings, Field


class RabbitConnectionSettings(BaseSettings):
    """DTO that represents the RabbitMQ connection."""

    url: str = Field(default=None)
    host: str = Field(default="localhost")
    port: int = Field(default=5627)
    login: str = Field(default="guest")
    password: str = Field(default="guest")
    virtualhost: str = Field(default="/")
    ssl: bool = Field(default=False)
    ssl_options: Optional[SSLOptions] = Field(default=None)
    ssl_context: Optional[SSLContext] = Field(default=None)
    timeout: Optional[Union[int, float]] = Field(default=None)
    client_properties: Optional[Dict[str, Union[float, int]]] = Field(default=None)


__all__ = ("RabbitConnectionSettings",)
