from __future__ import annotations

from constants import (
    ACTIVE_SLOT_STATUS,
    CAPACITY_GROWTH_FACTOR,
    CAPACITY_GROWTH_OFFSET,
    DEFAULT_BASE_ADDRESS,
    DEFAULT_INITIAL_CAPACITY,
    DEFAULT_MAX_LOAD_FACTOR,
    DEFAULT_REHASH_OCCUPANCY_FACTOR,
    DELETED_SLOT_STATUS,
    EMPTY_SLOT_STATUS,
)
from exceptions import DuplicateKeyError, KeyNotFoundError
from hashing import compute_base_hash, compute_v_value, normalize_key
from models import HashEntry, HashSlot, TableRow


def _is_prime(number: int) -> bool:
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def _next_prime(number: int) -> int:
    candidate = max(2, number)
    while not _is_prime(candidate):
        candidate += 1
    return candidate


class QuadraticProbingHashTable:
    def __init__(
        self,
        initial_capacity: int = DEFAULT_INITIAL_CAPACITY,
        base_address: int = DEFAULT_BASE_ADDRESS,
        max_load_factor: float = DEFAULT_MAX_LOAD_FACTOR,
        rehash_occupancy_factor: float = DEFAULT_REHASH_OCCUPANCY_FACTOR,
    ) -> None:
        if max_load_factor <= 0 or max_load_factor >= 1:
            raise ValueError("max_load_factor must be between 0 and 1.")
        if rehash_occupancy_factor <= 0 or rehash_occupancy_factor > 1:
            raise ValueError("rehash_occupancy_factor must be between 0 and 1.")
        self._capacity = _next_prime(initial_capacity)
        self._base_address = base_address
        self._max_load_factor = max_load_factor
        self._rehash_occupancy_factor = rehash_occupancy_factor
        self._active_count = 0
        self._deleted_count = 0
        self._slots = [HashSlot() for _ in range(self._capacity)]

    @property
    def capacity(self) -> int:
        return self._capacity

    def create(self, key: str, value: str) -> None:
        normalized_key = normalize_key(key)
        normalized_value = self._normalize_value(value)
        self._insert_entry(normalized_key, normalized_value)

    def read(self, key: str) -> str | None:
        normalized_key = normalize_key(key)
        index = self._probe_for_search(normalized_key)
        if index is None:
            return None
        return self._slots[index].entry.value

    def update(self, key: str, value: str) -> None:
        normalized_key = normalize_key(key)
        index = self._probe_for_search(normalized_key)
        if index is None:
            raise KeyNotFoundError(f"Key '{normalized_key}' does not exist.")
        slot = self._slots[index]
        entry = slot.entry
        slot.entry = HashEntry(entry.key, self._normalize_value(value), entry.v_value, entry.base_hash)

    def delete(self, key: str) -> None:
        normalized_key = normalize_key(key)
        index = self._probe_for_search(normalized_key)
        if index is None:
            raise KeyNotFoundError(f"Key '{normalized_key}' does not exist.")
        self._slots[index] = HashSlot(status=DELETED_SLOT_STATUS, entry=None)
        self._active_count -= 1
        self._deleted_count += 1

    def load_factor(self) -> float:
        return self._active_count / self._capacity

    def to_rows(self) -> list[TableRow]:
        chain_by_index = self._build_chain_metadata()
        rows: list[TableRow] = []
        for index, slot in enumerate(self._slots):
            if slot.is_active():
                entry = slot.entry
                chain = chain_by_index.get(index, [index])
                current_position = chain.index(index)
                is_terminal = current_position == len(chain) - 1
                next_pointer = index if is_terminal else chain[current_position + 1]
                collision_flag = int(len(chain) > 1)
                rows.append(
                    TableRow(
                        index=index,
                        status=slot.status,
                        id_value=entry.key,
                        collision_flag=collision_flag,
                        used_flag=1,
                        terminal_flag=int(is_terminal),
                        link_flag=0,
                        deleted_flag=0,
                        overflow_pointer=next_pointer,
                        pointer_or_data=entry.value,
                        key=entry.key,
                        value=entry.value,
                        v_value=entry.v_value,
                        base_hash=entry.base_hash,
                    )
                )
                continue
            is_deleted = slot.status == DELETED_SLOT_STATUS
            rows.append(
                TableRow(
                    index=index,
                    status=slot.status,
                    id_value=None,
                    collision_flag=0,
                    used_flag=0,
                    terminal_flag=1,
                    link_flag=0,
                    deleted_flag=int(is_deleted),
                    overflow_pointer=None,
                    pointer_or_data=None,
                    key=None,
                    value=None,
                    v_value=None,
                    base_hash=None,
                )
            )
        return rows

    def _normalize_value(self, value: str) -> str:
        if not isinstance(value, str):
            return str(value)
        return value

    def _insert_entry(self, normalized_key: str, normalized_value: str) -> None:
        if self._should_resize_before_insert():
            self._resize_and_rehash(self._growing_capacity())
        while True:
            base_hash = self._base_hash_for_key(normalized_key)
            index, is_duplicate = self._probe_for_insert(normalized_key, base_hash)
            if is_duplicate:
                raise DuplicateKeyError(f"Key '{normalized_key}' already exists.")
            if index is not None:
                self._place_entry(index, normalized_key, normalized_value, base_hash)
                return
            self._resize_and_rehash(self._growing_capacity())

    def _should_resize_before_insert(self) -> bool:
        projected_load = (self._active_count + 1) / self._capacity
        occupied_ratio = (self._active_count + self._deleted_count + 1) / self._capacity
        if projected_load > self._max_load_factor:
            return True
        return occupied_ratio > self._rehash_occupancy_factor

    def _base_hash_for_key(self, normalized_key: str) -> int:
        v_value = compute_v_value(normalized_key)
        return compute_base_hash(v_value, self._capacity, self._base_address)

    def _probe_indices(self, base_hash: int):
        for step in range(self._capacity):
            yield (base_hash + step * step) % self._capacity

    def _probe_for_insert(self, normalized_key: str, base_hash: int) -> tuple[int | None, bool]:
        first_deleted_index: int | None = None
        for index in self._probe_indices(base_hash):
            slot = self._slots[index]
            if slot.status == EMPTY_SLOT_STATUS:
                if first_deleted_index is not None:
                    return first_deleted_index, False
                return index, False
            if slot.status == DELETED_SLOT_STATUS and first_deleted_index is None:
                first_deleted_index = index
                continue
            if slot.is_active() and slot.entry.key == normalized_key:
                return index, True
        if first_deleted_index is not None:
            return first_deleted_index, False
        return None, False

    def _probe_for_search(self, normalized_key: str) -> int | None:
        base_hash = self._base_hash_for_key(normalized_key)
        for index in self._probe_indices(base_hash):
            slot = self._slots[index]
            if slot.status == EMPTY_SLOT_STATUS:
                return None
            if slot.is_active() and slot.entry.key == normalized_key:
                return index
        return None

    def _place_entry(self, index: int, key: str, value: str, base_hash: int) -> None:
        if self._slots[index].status == DELETED_SLOT_STATUS:
            self._deleted_count -= 1
        entry = HashEntry(key=key, value=value, v_value=compute_v_value(key), base_hash=base_hash)
        self._slots[index] = HashSlot(status=ACTIVE_SLOT_STATUS, entry=entry)
        self._active_count += 1

    def _growing_capacity(self) -> int:
        return self._capacity * CAPACITY_GROWTH_FACTOR + CAPACITY_GROWTH_OFFSET

    def _resize_and_rehash(self, target_capacity: int) -> None:
        active_entries = [slot.entry for slot in self._slots if slot.is_active()]
        self._capacity = _next_prime(target_capacity)
        self._slots = [HashSlot() for _ in range(self._capacity)]
        self._active_count = 0
        self._deleted_count = 0
        for entry in active_entries:
            self._rehash_entry(entry)

    def _rehash_entry(self, entry: HashEntry) -> None:
        base_hash = self._base_hash_for_key(entry.key)
        index, is_duplicate = self._probe_for_insert(entry.key, base_hash)
        if is_duplicate or index is None:
            raise RuntimeError("Rehash failed unexpectedly.")
        self._slots[index] = HashSlot(status=ACTIVE_SLOT_STATUS, entry=HashEntry(entry.key, entry.value, entry.v_value, base_hash))
        self._active_count += 1

    def _build_chain_metadata(self) -> dict[int, list[int]]:
        grouped_indices: dict[int, list[int]] = {}
        for index, slot in enumerate(self._slots):
            if slot.is_active():
                base_hash = slot.entry.base_hash
                grouped_indices.setdefault(base_hash, []).append(index)
        chain_by_index: dict[int, list[int]] = {}
        for base_hash, indices in grouped_indices.items():
            ordered_chain = sorted(indices, key=lambda current_index: self._probe_rank(base_hash, current_index))
            for chain_index in ordered_chain:
                chain_by_index[chain_index] = ordered_chain
        return chain_by_index

    def _probe_rank(self, base_hash: int, index: int) -> int:
        for step in range(self._capacity):
            if (base_hash + step * step) % self._capacity == index:
                return step
        return self._capacity
