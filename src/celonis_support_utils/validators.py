"""Shared validation utilities for domain classes."""

from .enums import Region


def parse_region(value: str) -> Region:
    try:
        return Region[value.strip().upper()]
    except KeyError as exc:
        valid_regions = [r.name for r in Region]
        raise ValueError(
            f"Invalid region: {exc}. Must be one of {valid_regions}"
        ) from exc


def require_non_empty(value: str, field_name: str) -> str:
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty")
    return value.strip()
