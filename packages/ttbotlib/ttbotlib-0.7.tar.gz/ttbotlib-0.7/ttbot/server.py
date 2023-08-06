import base64
import hmac
import json
import logging
import os
import mimetypes
import itertools

from hashlib import sha256
from pathlib import Path
from urllib.parse import parse_qs

from ttutils import to_bytes

from .client import Client
from .types import Action, Post, Receive, Request, Scope, Send


class Server:
    client: Client
    url_prefix: str
    __secret_bytes__: bytes

    log = logging.getLogger('server')

    def __init__(self, secret: str = '', static_path: str = '') -> None:
        secret = secret or os.environ.get('SECRET', '')
        assert secret, 'Set SECRET env'

        self.url_prefix = '/' + secret[:8]
        self.client = Client(secret[20:])
        self.__secret_bytes__ = to_bytes(int(secret, 32))

        self._static_files: dict[str, dict] = {}
        if base_path := os.environ.get('STATIC', static_path):
            self._load_static_files(base_path)

    def _load_static_files(self, base_path: str) -> None:
        all_files = itertools.chain(*[
            [Path(prefix) / Path(fname) for fname in files]
            for prefix, _, files in os.walk(base_path)
        ])

        for path in all_files:
            with open(path, 'rb') as fh:
                content_length = str(os.fstat(fh.fileno()).st_size)
                content_type, _ = mimetypes.guess_type(path.name)

                self._static_files[str(path).replace(base_path, '')] = {
                    'content_length': bytes(content_length, 'utf8'),
                    'content_type': bytes(content_type or '', 'utf8'),
                    'body': fh.read(),
                }

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ''' Main http router '''
        # Remove guard path prefix
        scope['path'] = scope['path'].replace(self.url_prefix, '') or '/'

        match scope:
            case {'type': 'http', 'method': 'POST', 'path': '/' | '/bot'}:
                await self.asgi_call_bot(scope, receive, send)
            case {'type': 'http', 'method': 'POST', 'path': '/act'}:
                await self.asgi_call_act(scope, receive, send)
            case {'type': 'http', 'path': '/api'}:
                await self.asgi_call_api(scope, receive, send)
            case {'type': 'websocket', 'path': '/shell'}:
                await self.asgi_call_shell(scope, receive, send)
            case {'type': 'http', 'path': path}:
                if path.startswith('/static'):
                    await self.lightweight_static(path.replace('/static', ''), send)
                else:
                    await self.send_404(send)
            case _:
                await self._send_json({'error': 'unknown path'}, send)

    async def lightweight_static(self, path: str, send: Send) -> None:
        if file_data := self._static_files.get(path):
            await send({
                'type': 'http.response.start',
                'status': 200,
                'headers': [
                    [b'content-type', file_data['content_type']],
                    [b'content-length', file_data['content_length']],
                ]
            })

            await send({
                'type': 'http.response.body',
                'body': file_data['body'],
            })

        else:
            await self.send_404(send)

    async def send_404(self, send: Send) -> None:
        await send({'type': 'http.response.start', 'status': 404})
        await send({'type': 'http.response.body', 'body': ''})

    # ASGI API
    async def asgi_call_api(self, scope: Scope, receive: Receive, send: Send) -> None:
        ''' HTTP API with ASGI interface '''

        headers = {
            str(key, 'utf8'): str(val, 'utf8')
            for key, val in scope.get('headers', [])
        }
        query = {
            key: val[0] if len(val) == 1 else val for key, val in
            parse_qs(str(scope.get('query_string', b''), 'utf8')).items()
        }
        data = await self._load_json(scope, receive, False)

        request = Request(
            method=scope['method'],
            path=scope['path'],
            query=query,
            headers=headers,
            data=data
        )

        response = await self.api_handler(request)
        await self._send_json(response, send)

    async def asgi_call_act(self, scope: Scope, receive: Receive, send: Send) -> None:
        ''' Action endpoint with ASGI interface '''
        data = await self._load_json(scope, receive)

        if missed_fields := {'user_id', 'chat_id', 'post_no', 'action'} - set(data.keys()):
            await self._send_json({'error': f'Missed fields: {missed_fields}'}, send)
            return None

        action = Action(
            user_id=data.pop('user_id'),
            action=data.pop('action'),
            params=data,
            post=Post(
                user_id=0,
                chat_id=data.pop('chat_id'),
                post_no=data.pop('post_no'),
                team_id=data.pop('organization_id', None),
                text=data.pop('text', '')
            )
        )

        response = await self.action_handler(action)
        await self._send_json(response, send)

    async def asgi_call_bot(self, scope: Scope, receive: Receive, send: Send) -> None:
        ''' Bot endpoint with ASGI interface '''
        data = await self._load_json(scope, receive)

        if missed_fields := {'user_id', 'chat_id', 'post_no', 'text'} - set(data.keys()):
            await self._send_json({'error': f'Missed fields: {missed_fields}'}, send)
            return None

        post = Post(
            user_id=data['user_id'],
            chat_id=data['chat_id'],
            post_no=data['post_no'],
            text=data['text'],
            team_id=data.get('organization_id'),
            reply_no=data.get('reply_no'),
            reply_text=data.get('reply_text')
        )

        answer = await self.message_handler(post)
        await self._send_json({'text': answer}, send)

    async def asgi_call_shell(self, scope: Scope, receive: Receive, send: Send) -> None:
        pass

    async def _send_json(self, data: dict, send: Send) -> None:
        ''' Send json http response '''
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'application/json'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps(
                data,
                ensure_ascii=False,
                allow_nan=False,
                indent=None,
                separators=(',', ':'),
            ).encode('utf-8')
        })

    async def _load_json(self, scope: Scope, receive: Receive, signed: bool = True) -> dict:
        '''
            Loading json-data from http-body over receive ASGI-function.
            If signed is true, will be checking body signature with x-signature header
        '''
        signature = dict(scope.get('headers', {})).get(b'x-signature')
        body = b''
        more_body = True

        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        if body and signed and self._make_signature(body) != signature:
            self.log.warning('Incorrect signature %s != %s', signature, self._make_signature(body))

        return json.loads(body) if body else {}

    def _make_signature(self, val: bytes) -> bytes:
        ''' Make signature for body (bytes) '''
        return base64.b64encode(hmac.new(self.__secret_bytes__, val, digestmod=sha256).digest())

    # handlers
    async def message_handler(self, post: Post) -> str:
        self.log.info('Get message %s', post)
        raise NotImplementedError

    async def action_handler(self, action: Action) -> dict:
        self.log.info('Call action %s', action)
        raise NotImplementedError

    async def api_handler(self, request: Request) -> dict:
        self.log.info('API call %s', request)
        raise NotImplementedError
