"""
Amount Parser Module

This module provides utilities for parsing and extracting monetary amounts
from grant information strings in various formats.

Supported formats:
- $5,000
- Up to $50,000
- $5,000 - $10,000 (range)
- $1000000
- Between $10,000 and $50,000
"""

import re
from typing import Optional, Tuple


def extract_amount_value(amount_str: str) -> int:
    """
    Extract the first numeric amount from a string.
    
    Handles various formats including currency symbols, commas, and ranges.
    Returns the minimum value in case of ranges.
    
    Args:
        amount_str (str): The amount string to parse (e.g., "$5,000", "Up to $50,000").
    
    Returns:
        int: The extracted amount as an integer, or 0 if no amount found.
    
    Example:
        >>> extract_amount_value("$5,000")
        5000
        
        >>> extract_amount_value("Up to $50,000")
        50000
        
        >>> extract_amount_value("$5,000 - $10,000")
        5000
        
        >>> extract_amount_value("No amount specified")
        0
    """
    if not amount_str:
        return 0
    
    # Find all currency amounts in the string
    # Pattern matches: $1000, $1,000, $1,000,000, etc.
    matches = re.findall(r'\$[\d,]+', amount_str)
    
    if not matches:
        return 0
    
    # Extract the first (minimum) amount
    first_match = matches[0]
    # Remove $ and commas, then convert to int
    return int(first_match.replace('$', '').replace(',', ''))


def parse_amount_range(amount_str: str) -> Tuple[int, Optional[int]]:
    """
    Parse an amount string and return minimum and maximum values.
    
    Handles ranges like "$5,000 - $10,000" and single values like "Up to $50,000".
    
    Args:
        amount_str (str): The amount string to parse.
    
    Returns:
        Tuple[int, Optional[int]]: (minimum_amount, maximum_amount).
                                   maximum_amount is None for single values.
    
    Example:
        >>> parse_amount_range("$5,000 - $10,000")
        (5000, 10000)
        
        >>> parse_amount_range("Up to $50,000")
        (0, 50000)
        
        >>> parse_amount_range("$5,000")
        (5000, None)
    """
    if not amount_str:
        return (0, None)
    
    # Find all currency amounts
    matches = re.findall(r'\$[\d,]+', amount_str)
    
    if not matches:
        return (0, None)
    
    # Convert matches to integers
    amounts = [int(m.replace('$', '').replace(',', '')) for m in matches]
    
    if len(amounts) == 1:
        # Single value - check if it's a range or maximum
        if "up to" in amount_str.lower() or "maximum" in amount_str.lower():
            return (0, amounts[0])
        else:
            return (amounts[0], None)
    else:
        # Range - return min and max
        return (min(amounts), max(amounts))


def format_amount(amount: int) -> str:
    """
    Format an integer amount as a currency string.
    
    Args:
        amount (int): The amount to format.
    
    Returns:
        str: Formatted amount string (e.g., "$5,000").
    
    Example:
        >>> format_amount(5000)
        '$5,000'
        
        >>> format_amount(1000000)
        '$1,000,000'
    """
    return f"${amount:,}"


def is_amount_in_range(
    amount: int,
    min_threshold: int,
    max_threshold: Optional[int] = None
) -> bool:
    """
    Check if an amount falls within a specified range.
    
    Args:
        amount (int): The amount to check.
        min_threshold (int): Minimum threshold (inclusive).
        max_threshold (Optional[int]): Maximum threshold (inclusive).
                                       If None, only checks minimum.
    
    Returns:
        bool: True if amount is within range, False otherwise.
    
    Example:
        >>> is_amount_in_range(7500, 5000, 10000)
        True
        
        >>> is_amount_in_range(7500, 10000)
        False
        
        >>> is_amount_in_range(7500, 5000)
        True
    """
    if amount < min_threshold:
        return False
    
    if max_threshold is not None and amount > max_threshold:
        return False
    
    return True
