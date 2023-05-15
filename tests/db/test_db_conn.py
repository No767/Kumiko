import sys
from pathlib import Path

from prisma.utils import async_run

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))


from Libs.utils.postgresql import PrismaSessionManager
from prisma.models import User


def test_prisma_client_session_manager():
    with PrismaSessionManager():
        res = async_run(User.prisma().find_first(where={"id": 454357482102587393}))
        assert (res is None) or (isinstance(res, User))  # nosec
