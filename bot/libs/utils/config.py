import asyncio
import os
import uuid
from pathlib import Path
from typing import Any, Dict, Generic, Optional, TypeVar, Union, overload

import msgspec
import yaml

_T = TypeVar("_T")


class KumikoConfig(Generic[_T]):
    def __init__(self, path: Path):
        self.path = path
        self._config: Dict[str, Union[_T, Any]] = {}
        self.load_from_file()

    def load_from_file(self) -> None:
        try:
            with open(self.path, "r") as f:
                self._config: Dict[str, Union[_T, Any]] = yaml.safe_load(f.read())
        except FileNotFoundError:
            self._config = {}

    @property
    def kumiko(self) -> _T:
        return self._config["kumiko"]

    @overload
    def get(self, key: Any) -> Optional[Union[_T, Any]]: ...

    @overload
    def get(self, key: Any, default: Any) -> Union[_T, Any]: ...

    def get(self, key: Any, default: Any = None) -> Optional[Union[_T, Any]]:
        """Retrieves a config entry."""
        return self._config.get(str(key), default)

    def __contains__(self, item: Any) -> bool:
        return str(item) in self._config

    def __getitem__(self, item: Any) -> Union[_T, Any]:
        return self._config[str(item)]

    def __len__(self) -> int:
        return len(self._config)

    def all(self) -> dict[str, Union[_T, Any]]:
        return self._config


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

    def load_from_file(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self._db = msgspec.json.decode(f.read())
        except FileNotFoundError:
            self._db = {}

    async def load(self):
        async with self.lock:
            await self.loop.run_in_executor(None, self.load_from_file)

    def _dump(self):
        temp = f"{uuid.uuid4()}-{self.path.stem}.tmp"
        with open(temp, "w", encoding="utf-8") as tmp:
            encoded = msgspec.json.format(
                self.encoder.encode(self._db.copy()), indent=2
            )
            tmp.write(encoded.decode())

        # atomically move the file
        os.replace(temp, self.path)

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
