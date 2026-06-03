"""
Utility modules for the Grant Research Website project.

This package contains utilities for:
- Loading configuration files (config_loader)
- Parsing dates in various formats (date_parser)
- Parsing monetary amounts (amount_parser)
- Removing duplicate grants (deduplicator)
"""

from .config_loader import ConfigLoader
from .date_parser import parse_deadline, is_deadline_open, format_deadline
from .amount_parser import extract_amount_value, parse_amount_range, format_amount
from .deduplicator import deduplicate_grants, find_duplicates

__all__ = [
    'ConfigLoader',
    'parse_deadline',
    'is_deadline_open',
    'format_deadline',
    'extract_amount_value',
    'parse_amount_range',
    'format_amount',
    'deduplicate_grants',
    'find_duplicates',
]
