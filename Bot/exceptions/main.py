class Error(Exception):
    pass


class UnknownPlayer(Error):
    pass


class NotFoundHTTPException(Error):
    pass


class NoItemsError(Error):
    pass


class ThereIsaRSlashInSubreddit(Error):
    pass


class HTTPException(Error):
    pass


class InvalidToken(Error):
    pass
