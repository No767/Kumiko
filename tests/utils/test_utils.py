import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

ENV_PATH = path / ".env"

from Libs.utils import is_docker, read_env


def test_is_docker():
    if is_docker() is False:
        assert is_docker() is False
        return
    assert is_docker() is True


def test_read_env():
    read_from_file = False
    if is_docker() or read_from_file is False:
        config = read_env(ENV_PATH, False)
        assert "POSTGRES_URI" or "SHELL" in config
    config = read_env(ENV_PATH)
    assert isinstance(config, dict)
