from typing import Any, Union

import ormsgpack

from .base import BaseSerializer


class MsgPackSerializer(BaseSerializer):
    """Serializes data to msgpack using ormsgpack"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def dumps(self, value: Any) -> bytes:
        """Serializes a value

        Args:
            value (Any): The value to serialize

        Returns:
            bytes: The serialized value now in msgpack format
        """
        return ormsgpack.packb(value)

    def loads(self, value: Union[bytes, None]) -> Any:
        """Deserializes a value

        Args:
            value (bytes): The value to deserialize

        Returns:
            Any: The deserialized value
        """
        if value is None:
            return None
        return ormsgpack.unpackb(value)
