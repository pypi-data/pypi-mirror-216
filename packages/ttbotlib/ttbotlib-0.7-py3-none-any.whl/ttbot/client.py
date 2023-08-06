import logging

import httpx


class Client:
    __secret__: str = ''
    host: str = ''
    log = logging.getLogger('client')

    def __init__(self, secret: str, host: str = 'api.pararam.io') -> None:
        self.__secret__ = secret
        self.host = f'https://{host}'

    def __repr__(self) -> str:
        return f'Client [{self.host}]' + (' with ' if self.__secret__ else ' no ') + 'secret'

    async def api_call(self, uri: str, method: str = 'GET', data: dict = {}) -> dict:
        async with httpx.AsyncClient(headers={'X-APIToken': self.__secret__}) as client:
            resp = await client.request(method, f'{self.host}{uri}', json=data)
            self.log.info('API %s %s: %s', method, uri, resp.status_code)
            return resp.json()

    async def send_post(self, chat_id: int, text: str) -> None:
        data = {'chat_id': chat_id, 'text': text}
        await self.api_call('/bot/message', 'POST', data)

    async def send_private_post(self, user_id: int, text: str) -> None:
        data = {'user_id': user_id, 'text': text}
        await self.api_call('/msg/post/private', 'POST', data)
