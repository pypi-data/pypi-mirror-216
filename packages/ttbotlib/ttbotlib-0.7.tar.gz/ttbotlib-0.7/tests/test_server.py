from unittest.mock import AsyncMock

import pytest

from ttbot import Action, Post, Request, Server


class TestServer(Server):
    async def message_handler(self, post: Post) -> str:
        return 'test'

    async def action_handler(self, action: Action) -> dict:
        assert action == Action(
            action='check',
            user_id=1,
            params={'param1': 7},
            post=Post(user_id=0, chat_id=2, post_no=3, team_id=None, text='')
        )
        return {'res': '№'}

    async def api_handler(self, request: Request) -> dict:
        assert request == Request(
            method='POST',
            path='/api',
            query={'a': '1', 'b': ['2', '3']},
            headers={'Key': 'Value'},
            data={'q': 1}
        )
        return {'res': 'Куй'}


@pytest.fixture(scope='module')
def server():
    return TestServer()


async def test_api_interface_ok():
    with pytest.raises(NotImplementedError):
        request = Request(method='POST', path='/api', query={}, headers={}, data={})
        await Server().api_handler(request)


async def test_act_interface_ok():
    with pytest.raises(NotImplementedError):
        post = Post(user_id=0, chat_id=2, post_no=3, text='')
        await Server().action_handler(Action(post=post, action='act', params={}, user_id=1))


async def test_bot_interface_ok():
    with pytest.raises(NotImplementedError):
        await Server().message_handler(Post(user_id=1, chat_id=2, post_no=3, text=''))


async def test_api_ok(server):
    receive = AsyncMock(return_value={'body': b'{"q":1}'})
    send = AsyncMock()

    await server({'type': 'http', 'method': 'POST', 'path': '/api', 'query_string': b'a=1&b=2&b=3',
        'headers': [[b'Key', b'Value']]}, receive, send)

    assert send.call_args_list[0][0][0] == {
        'type': 'http.response.start', 'status': 200,
        'headers': [[b'content-type', b'application/json']]
    }
    assert send.call_args_list[1][0][0] == {
        'type': 'http.response.body', 'body': b'{"res":"\xd0\x9a\xd1\x83\xd0\xb9"}'
    }


async def test_act_ok(server):
    send = AsyncMock()
    receive = AsyncMock(return_value={
        'body': b'{"action":"check","user_id":1,"chat_id":2,"post_no":3,"param1":7}'
    })

    await server({'type': 'http', 'method': 'POST', 'path': '/act',
        'headers': [[b'x-signature', b'Value']]}, receive, send)

    assert send.call_args_list[0][0][0] == {
        'type': 'http.response.start', 'status': 200,
        'headers': [[b'content-type', b'application/json']]
    }
    assert send.call_args_list[1][0][0] == {
        'type': 'http.response.body', 'body': b'{"res":"\xe2\x84\x96"}'
    }


async def test_act_ok_error(server):
    send = AsyncMock()
    receive = AsyncMock(return_value={'body': b'{"action":"check","user_id":1,"chat_id":2}'})

    await server({'type': 'http', 'method': 'POST', 'path': '/act',
        'headers': [[b'x-signature', b'Value']]}, receive, send)

    assert send.call_args_list[1][0][0] == {
        'type': 'http.response.body', 'body': b'{"error":"Missed fields: {\'post_no\'}"}'
    }


async def test_bot_ok(server):
    send = AsyncMock()
    receive = AsyncMock(return_value={
        'body': b'{"user_id":1,"chat_id":2,"post_no":3,"text":"text","team_id":4}'
    })

    await server({'type': 'http', 'method': 'POST', 'path': '/',
        'headers': [[b'x-signature', b'Value']]}, receive, send)

    assert send.call_args_list[0][0][0] == {
        'type': 'http.response.start', 'status': 200,
        'headers': [[b'content-type', b'application/json']]
    }
    assert send.call_args_list[1][0][0] == {
        'type': 'http.response.body', 'body': b'{"text":"test"}'
    }


async def test_bot_ok_error(server):
    send = AsyncMock()
    receive = AsyncMock(return_value={'body': b'{"user_id":1,"chat_id":2,"text":"text"}'})

    await server({'type': 'http', 'method': 'POST', 'path': '/bot',
        'headers': [[b'x-signature', b'Value']]}, receive, send)

    assert send.call_args_list[1][0][0] == {
        'type': 'http.response.body', 'body': b'{"error":"Missed fields: {\'post_no\'}"}'
    }


async def test_unknown_ok(server):
    send = AsyncMock()
    receive = AsyncMock(return_value={'body': b''})

    await server({'type': 'http', 'method': 'POST', 'path': '/qwe'}, receive, send)

    assert send.call_args_list[1][0][0] == {'type': 'http.response.body', 'body': ''}


async def test_shell_ok(server):  # not ready
    receive = AsyncMock(return_value={'body': b'{"q":1}'})
    send = AsyncMock()

    await server({'type': 'websocket', 'path': '/shell'}, receive, send)
