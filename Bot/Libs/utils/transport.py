from aiohttp import ClientSession
from gql.transport.aiohttp import AIOHTTPTransport


class AIOHTTPTransportExistingSession(AIOHTTPTransport):
    def __init__(self, *args, client_session: ClientSession, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = client_session

    async def connect(self) -> None:
        pass

    async def close(self) -> None:
        pass
