from __future__ import annotations

from dataclasses import dataclass

from constants import ACTIVE_SLOT_STATUS, EMPTY_SLOT_STATUS


@dataclass(frozen=True)
class HashEntry:
    key: str
    value: str
    v_value: int
    base_hash: int


@dataclass
class HashSlot:
    status: str = EMPTY_SLOT_STATUS
    entry: HashEntry | None = None

    def is_active(self) -> bool:
        return self.status == ACTIVE_SLOT_STATUS and self.entry is not None


@dataclass(frozen=True)
class TableRow:
    index: int
    status: str
    id_value: str | None
    collision_flag: int
    used_flag: int
    terminal_flag: int
    link_flag: int
    deleted_flag: int
    overflow_pointer: int | None
    pointer_or_data: str | None
    key: str | None
    value: str | None
    v_value: int | None
    base_hash: int | None
