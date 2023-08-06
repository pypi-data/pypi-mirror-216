import typing

from dataclasses import dataclass


Scope = typing.MutableMapping[str, typing.Any]
Message = typing.MutableMapping[str, typing.Any]

Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]


@dataclass
class Post:
    user_id: int
    chat_id: int
    post_no: int
    text: str
    reply_no: int | None = None
    reply_text: str | None = None
    team_id: int | None = None


@dataclass
class Request:
    method: str
    path: str
    query: dict
    headers: dict
    data: dict


@dataclass
class Action:
    user_id: int
    post: Post
    action: str
    params: dict
