import enum
import socket
from typing import List, Optional, Union

import pydantic
import pynng

from .base import Base


class Parameter(Base):
    key: str
    default: str = None
    value: str = None
    type: str


class Info(Base):
    type: str
    version: str
    parameters: List[Parameter]
    routes: List[str]


class Database(Base):
    user: str
    password: str
    netloc: str
    port: int
    dbname: str


class SocketType(enum.Enum):
    REQUESTER = pynng.Req0
    REPLIER = pynng.Rep0
    PUBLISHER = pynng.Pub0
    SUBSCRIBER = pynng.Sub0


class SocketConfig(Base):
    socket_type: Union[SocketType, str] = SocketType.REPLIER
    host: str = socket.gethostbyname(socket.gethostname())
    port: int = 0
    listen: bool = True
    recv_timeout: int = 500
    send_timeout: int = 500

    @pydantic.validator("socket_type")
    def validate_socket_type(cls, v):
        if type(v) is str:
            return getattr(SocketType, v.upper())
        return v

    def dict(self, *args, **kwargs):
        return {
            "socket_type": self.socket_type.name,
            "host": self.host,
            "port": self.port,
            "listen": self.listen,
            "recv_timeout": self.recv_timeout,
            "send_timeout": self.send_timeout,
        }

    def dump(self):
        return self.dict()


class Request(Base):
    task: str
    data: Optional[dict] = None
    error: Optional[str] = None


class Response(Base):
    task: str
    error: Optional[str] = None
    data: Optional[dict] = None
