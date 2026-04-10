class HashTableError(Exception):
    """Base exception for hash table errors."""


class DuplicateKeyError(HashTableError):
    """Raised when trying to create a record for an existing key."""


class KeyNotFoundError(HashTableError):
    """Raised when a key is not found for update/delete."""


class InvalidKeyError(HashTableError):
    """Raised when key cannot be normalized or hashed."""
