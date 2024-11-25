from pathlib import Path
from typing import Any, Dict, Generic, Optional, TypeVar, Union, overload

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
