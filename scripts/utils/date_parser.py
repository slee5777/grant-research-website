"""
Date Parser Module

This module provides utilities for parsing and validating deadline dates
in various formats commonly found in grant information.

Supported formats:
- 4 June 2026 (day month year)
- 04/06/2026 (day/month/year)
- 06/04/2026 (month/day/year)
- 2026-06-04 (ISO format)
- June 4, 2026 (month day, year)
- 4 Jun 2026 (day abbreviated_month year)
- Rolling Rounds (special case - always open)
"""

from datetime import datetime
from typing import Optional


# Supported date formats for parsing
DATE_FORMATS = [
    "%d %B %Y",      # 4 June 2026
    "%d/%m/%Y",      # 04/06/2026
    "%m/%d/%Y",      # 06/04/2026
    "%Y-%m-%d",      # 2026-06-04
    "%B %d, %Y",     # June 4, 2026
    "%d %b %Y",      # 4 Jun 2026
    "%d %B %y",      # 4 June 26
    "%B %d, %y",     # June 4, 26
]


def parse_deadline(deadline_str: str) -> Optional[datetime]:
    """
    Parse a deadline string and return a datetime object.
    
    Attempts to parse the deadline using multiple common date formats.
    Returns None for "Rolling Rounds" or if the deadline cannot be parsed.
    
    Args:
        deadline_str (str): The deadline string to parse.
        
    Returns:
        Optional[datetime]: Parsed datetime object, or None if:
            - deadline_str is None or empty
            - deadline_str contains "rolling" (case-insensitive)
            - deadline_str cannot be parsed with any supported format
    
    Example:
        >>> parse_deadline("4 June 2026")
        datetime.datetime(2026, 6, 4, 0, 0)
        
        >>> parse_deadline("Rolling Rounds")
        None
        
        >>> parse_deadline("invalid date")
        None
    """
    if not deadline_str:
        return None
    
    # Check for rolling deadlines
    if "rolling" in deadline_str.lower():
        return None
    
    # Try each supported format
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(deadline_str.strip(), fmt)
        except ValueError:
            continue
    
    # If no format matched, log warning and return None
    print(f"  ⚠️ Could not parse deadline: {deadline_str}")
    return None


def is_deadline_open(
    deadline_str: str,
    run_date: Optional[datetime] = None
) -> Optional[bool]:
    """
    Check if a grant deadline is still open (after the run date).
    
    Args:
        deadline_str (str): The deadline string to check.
        run_date (Optional[datetime]): Reference date for comparison.
                                      Defaults to current date/time.
    
    Returns:
        Optional[bool]:
            - True: Deadline is in the future (still open)
            - False: Deadline is in the past (closed)
            - None: Deadline is rolling or could not be parsed (treat as open)
    
    Example:
        >>> from datetime import datetime
        >>> is_deadline_open("4 June 2026", datetime(2026, 5, 1))
        True
        
        >>> is_deadline_open("4 June 2026", datetime(2026, 7, 1))
        False
        
        >>> is_deadline_open("Rolling Rounds")
        None
    """
    if not deadline_str or "rolling" in deadline_str.lower():
        return None  # Rolling deadlines are always open
    
    deadline = parse_deadline(deadline_str)
    if deadline is None:
        return None  # Unknown deadline format, treat as open
    
    if run_date is None:
        run_date = datetime.now()
    
    # Deadline is open if it's after the run date
    return deadline > run_date


def format_deadline(deadline: datetime, format_str: str = "%d %B %Y") -> str:
    """
    Format a datetime object as a deadline string.
    
    Args:
        deadline (datetime): The datetime object to format.
        format_str (str): The format string to use.
                         Defaults to "%d %B %Y" (e.g., "4 June 2026").
    
    Returns:
        str: Formatted deadline string.
    
    Example:
        >>> deadline = datetime(2026, 6, 4)
        >>> format_deadline(deadline)
        '4 June 2026'
    """
    return deadline.strftime(format_str)
