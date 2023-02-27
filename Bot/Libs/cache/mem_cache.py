from typing import Any, Dict


class MemoryCache:
    """Synchronous memory cache implementation based off of aiocache"""

    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def get(self, key: str) -> Any:
        """Gets a value from the cache

        Args:
            key (str): The key to use

        Returns:
            Any: The value from the cache
        """
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> Any:
        """Sets a value in the cache

        Args:
            key (str): The key to use
            value (Any): The value to set

        Returns:
            Any: The set value from the cache
        """
        self._cache[key] = value
        return self._cache[key]

    def add(self, key: str, value: Any) -> Any:
        """Adds a value to the cache if it doesn't exist

        Args:
            key (str): The key to use
            value (Any): The value to set

        Raises:
            ValueError: If the key already exists

        Returns:
            Any: The set value from the cache
        """
        if key in self._cache:
            raise ValueError(f"Key {key} already exists. Please use .set to update it")
        return self.set(key=key, value=value)

    def delete(self, key: str) -> Dict[str, Any]:
        """Deletes a key from the cache

        Args:
            key (str): The key to delete

        Returns:
            Dict[str, Any]: The deleted key-value pair
        """
        return self._cache.pop(key, None)
