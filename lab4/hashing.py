from __future__ import annotations

from constants import (
    DEFAULT_BASE_ADDRESS,
    ENGLISH_ALPHABET,
    ENGLISH_ALPHABET_BASE,
    ENGLISH_ALPHABET_NAME,
    RUSSIAN_ALPHABET,
    RUSSIAN_ALPHABET_BASE,
    RUSSIAN_ALPHABET_NAME,
)
from exceptions import InvalidKeyError

RUSSIAN_INDEX_BY_LETTER = {letter: index for index, letter in enumerate(RUSSIAN_ALPHABET)}
ENGLISH_INDEX_BY_LETTER = {letter: index for index, letter in enumerate(ENGLISH_ALPHABET)}


def normalize_key(key: str) -> str:
    if not isinstance(key, str):
        raise InvalidKeyError("Key must be a string.")
    normalized_key = key.strip().upper()
    if not normalized_key:
        raise InvalidKeyError("Key must not be empty.")
    return normalized_key


def _extract_hash_letters(normalized_key: str) -> tuple[str, str, str]:
    supported_letters = [
        character
        for character in normalized_key
        if character in RUSSIAN_INDEX_BY_LETTER or character in ENGLISH_INDEX_BY_LETTER
    ]
    if len(supported_letters) < 2:
        raise InvalidKeyError("Key must contain at least two supported letters.")
    first_letter, second_letter = supported_letters[0], supported_letters[1]
    if first_letter in RUSSIAN_INDEX_BY_LETTER and second_letter in RUSSIAN_INDEX_BY_LETTER:
        return first_letter, second_letter, RUSSIAN_ALPHABET_NAME
    if first_letter in ENGLISH_INDEX_BY_LETTER and second_letter in ENGLISH_INDEX_BY_LETTER:
        return first_letter, second_letter, ENGLISH_ALPHABET_NAME
    raise InvalidKeyError("First two hash letters must belong to one alphabet.")


def _alphabet_config(alphabet_name: str) -> tuple[dict[str, int], int]:
    if alphabet_name == RUSSIAN_ALPHABET_NAME:
        return RUSSIAN_INDEX_BY_LETTER, RUSSIAN_ALPHABET_BASE
    return ENGLISH_INDEX_BY_LETTER, ENGLISH_ALPHABET_BASE


def compute_v_value(key: str) -> int:
    normalized_key = normalize_key(key)
    first_letter, second_letter, alphabet_name = _extract_hash_letters(normalized_key)
    index_by_letter, base = _alphabet_config(alphabet_name)
    return index_by_letter[first_letter] * base + index_by_letter[second_letter]


def compute_base_hash(
    v_value: int,
    capacity: int,
    base_address: int = DEFAULT_BASE_ADDRESS,
) -> int:
    if capacity <= 0:
        raise ValueError("Capacity must be positive.")
    if base_address < 0:
        raise ValueError("Base address must not be negative.")
    return (v_value % capacity + base_address) % capacity
