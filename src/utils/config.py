from __future__ import annotations

import asyncio
import uuid
from pathlib import Path
from typing import Any, Generic, Optional, TypeVar, Union, overload

import msgspec

_T = TypeVar("_T")


class PrometheusSettings(msgspec.Struct, frozen=True):
    enabled: bool
    host: str
    port: int


class KumikoConfig(msgspec.Struct, frozen=True):
    token: str
    dev_mode: bool
    prometheus: PrometheusSettings
    postgres_uri: str

    @classmethod
    def load_from_file(cls, path: Optional[Path]) -> KumikoConfig:
        if not path:
            raise FileNotFoundError("Configuration file not found")

        with path.open() as f:
            return msgspec.yaml.decode(f.read(), type=KumikoConfig)


class Blacklist(Generic[_T]):
    """Internal blacklist database used by R. Danny"""

    def __init__(
        self,
        path: Path,
        *,
        load_later: bool = False,
    ):
        self.path = path
        self.encoder = msgspec.json.Encoder()
        self.loop = asyncio.get_running_loop()
        self.lock = asyncio.Lock()
        self._db: dict[str, Union[_T, Any]] = {}
        if load_later:
            self.loop.create_task(self.load())
        else:
            self.load_from_file()

    def load_from_file(self) -> None:
        try:
            with self.path.open(encoding="utf-8") as f:
                self._db = msgspec.json.decode(f.read())
        except FileNotFoundError:
            self._db = {}

    async def load(self) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.load_from_file)

    def _dump(self):
        temp = Path(f"{uuid.uuid4()}-{self.path.stem}.tmp")

        with temp.open("w", encoded="utf-8") as tmp:
            encoded = msgspec.json.format(
                self.encoder.encode(self._db.copy()), indent=2
            )
            tmp.write(encoded.decode())

        # atomically move the file
        temp_path = Path(self.path)
        temp_path.replace(temp)

    async def save(self) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self._dump)

    @overload
    def get(self, key: Any) -> Optional[Union[_T, Any]]: ...

    @overload
    def get(self, key: Any, default: Any) -> Union[_T, Any]: ...

    def get(self, key: Any, default: Any = None) -> Optional[Union[_T, Any]]:
        """Retrieves a config entry."""
        return self._db.get(str(key), default)

    async def put(self, key: Any, value: Union[_T, Any]) -> None:
        """Edits a config entry."""
        self._db[str(key)] = value
        await self.save()

    async def remove(self, key: Any) -> None:
        """Removes a config entry."""
        del self._db[str(key)]
        await self.save()

    def __contains__(self, item: Any) -> bool:
        return str(item) in self._db

    def __getitem__(self, item: Any) -> Union[_T, Any]:
        return self._db[str(item)]

    def __len__(self) -> int:
        return len(self._db)

    def all(self) -> dict[str, Union[_T, Any]]:
        return self._db
