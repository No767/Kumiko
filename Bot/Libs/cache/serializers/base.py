from abc import ABC, abstractmethod
from typing import Any


class BaseSerializer(ABC):
    """An ABC for serializers"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @abstractmethod
    def dumps(self, value: Any) -> Any:
        """Serializes a value

        Args:
            value (Any): The value to serialize

        Returns:
            Any: The serialized value
        """

    @abstractmethod
    def loads(self, value: Any) -> Any:
        """Deserializes a value

        Args:
            value (Any): The value to deserialize

        Returns:
            Any: The deserialized value
        """
