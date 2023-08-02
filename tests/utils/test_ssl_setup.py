import ssl
import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.utils import setup_ssl


def test_setup_ssl():
    res = setup_ssl()
    is_hostnamed_enabled = res.check_hostname  # should be false
    is_verify_mode_enabled = res.verify_mode  # should be 0
    assert (
        is_hostnamed_enabled == False and is_verify_mode_enabled == 0
    ) and isinstance(res, ssl.SSLContext)
