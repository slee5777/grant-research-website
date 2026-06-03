"""
Unit Tests for Grant Research Website Utilities

Tests cover date parsing, amount parsing, deduplication, and configuration loading.
Run with: python -m pytest tests/test_utilities.py -v
"""

import unittest
from datetime import datetime
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from utils.date_parser import parse_deadline, is_deadline_open, format_deadline
from utils.amount_parser import extract_amount_value, parse_amount_range, format_amount, is_amount_in_range
from utils.deduplicator import deduplicate_grants, find_duplicates


class TestDateParser(unittest.TestCase):
    """Test cases for date parsing utilities."""
    
    def test_parse_deadline_uk_format(self):
        """Test parsing UK date format (day month year)."""
        result = parse_deadline("4 June 2026")
        self.assertIsNotNone(result)
        self.assertEqual(result.day, 4)
        self.assertEqual(result.month, 6)
        self.assertEqual(result.year, 2026)
    
    def test_parse_deadline_iso_format(self):
        """Test parsing ISO date format (YYYY-MM-DD)."""
        result = parse_deadline("2026-06-04")
        self.assertIsNotNone(result)
        self.assertEqual(result.day, 4)
        self.assertEqual(result.month, 6)
        self.assertEqual(result.year, 2026)
    
    def test_parse_deadline_us_format(self):
        """Test parsing US date format (month day, year)."""
        result = parse_deadline("June 4, 2026")
        self.assertIsNotNone(result)
        self.assertEqual(result.day, 4)
        self.assertEqual(result.month, 6)
    
    def test_parse_deadline_rolling(self):
        """Test that 'Rolling Rounds' returns None."""
        result = parse_deadline("Rolling Rounds")
        self.assertIsNone(result)
    
    def test_parse_deadline_empty(self):
        """Test that empty string returns None."""
        result = parse_deadline("")
        self.assertIsNone(result)
    
    def test_parse_deadline_invalid(self):
        """Test that invalid format returns None."""
        result = parse_deadline("invalid date")
        self.assertIsNone(result)
    
    def test_is_deadline_open_future(self):
        """Test that future deadline is open."""
        result = is_deadline_open("4 June 2026", datetime(2026, 5, 1))
        self.assertTrue(result)
    
    def test_is_deadline_open_past(self):
        """Test that past deadline is closed."""
        result = is_deadline_open("4 June 2026", datetime(2026, 7, 1))
        self.assertFalse(result)
    
    def test_is_deadline_open_rolling(self):
        """Test that rolling deadline returns None."""
        result = is_deadline_open("Rolling Rounds")
        self.assertIsNone(result)
    
    def test_format_deadline(self):
        """Test deadline formatting."""
        deadline = datetime(2026, 6, 4)
        result = format_deadline(deadline)
        self.assertEqual(result, "04 June 2026")


class TestAmountParser(unittest.TestCase):
    """Test cases for amount parsing utilities."""
    
    def test_extract_amount_value_simple(self):
        """Test extracting simple amount."""
        result = extract_amount_value("$5,000")
        self.assertEqual(result, 5000)
    
    def test_extract_amount_value_up_to(self):
        """Test extracting amount from 'Up to' format."""
        result = extract_amount_value("Up to $50,000")
        self.assertEqual(result, 50000)
    
    def test_extract_amount_value_range(self):
        """Test extracting minimum from range."""
        result = extract_amount_value("$5,000 - $10,000")
        self.assertEqual(result, 5000)
    
    def test_extract_amount_value_no_comma(self):
        """Test extracting amount without commas."""
        result = extract_amount_value("$5000")
        self.assertEqual(result, 5000)
    
    def test_extract_amount_value_empty(self):
        """Test that empty string returns 0."""
        result = extract_amount_value("")
        self.assertEqual(result, 0)
    
    def test_extract_amount_value_no_amount(self):
        """Test that string without amount returns 0."""
        result = extract_amount_value("No amount specified")
        self.assertEqual(result, 0)
    
    def test_parse_amount_range_single(self):
        """Test parsing single amount."""
        min_amt, max_amt = parse_amount_range("$5,000")
        self.assertEqual(min_amt, 5000)
        self.assertIsNone(max_amt)
    
    def test_parse_amount_range_up_to(self):
        """Test parsing 'Up to' format."""
        min_amt, max_amt = parse_amount_range("Up to $50,000")
        self.assertEqual(min_amt, 0)
        self.assertEqual(max_amt, 50000)
    
    def test_parse_amount_range_range(self):
        """Test parsing range format."""
        min_amt, max_amt = parse_amount_range("$5,000 - $10,000")
        self.assertEqual(min_amt, 5000)
        self.assertEqual(max_amt, 10000)
    
    def test_format_amount(self):
        """Test amount formatting."""
        result = format_amount(5000)
        self.assertEqual(result, "$5,000")
    
    def test_format_amount_large(self):
        """Test formatting large amount."""
        result = format_amount(1000000)
        self.assertEqual(result, "$1,000,000")
    
    def test_is_amount_in_range_within(self):
        """Test amount within range."""
        result = is_amount_in_range(7500, 5000, 10000)
        self.assertTrue(result)
    
    def test_is_amount_in_range_below(self):
        """Test amount below range."""
        result = is_amount_in_range(3000, 5000, 10000)
        self.assertFalse(result)
    
    def test_is_amount_in_range_above(self):
        """Test amount above range."""
        result = is_amount_in_range(15000, 5000, 10000)
        self.assertFalse(result)
    
    def test_is_amount_in_range_no_max(self):
        """Test amount with no maximum."""
        result = is_amount_in_range(7500, 5000)
        self.assertTrue(result)


class TestDeduplicator(unittest.TestCase):
    """Test cases for grant deduplication utilities."""
    
    def test_deduplicate_grants_no_duplicates(self):
        """Test that unique grants are not modified."""
        grants = [
            {"name": "Grant A", "deadline": "4 June 2026"},
            {"name": "Grant B", "deadline": "15 July 2026"},
        ]
        result = deduplicate_grants(grants)
        self.assertEqual(len(result), 2)
    
    def test_deduplicate_grants_with_duplicates(self):
        """Test that duplicates are removed."""
        grants = [
            {"name": "First Nations Arts Fund", "deadline": "15 July 2026"},
            {"name": "First Nations Arts Fund", "deadline": "30 June 2026"},
        ]
        result = deduplicate_grants(grants)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['deadline'], "15 July 2026")
    
    def test_deduplicate_grants_case_insensitive(self):
        """Test that deduplication is case-insensitive."""
        grants = [
            {"name": "Grant A", "deadline": "4 June 2026"},
            {"name": "grant a", "deadline": "15 July 2026"},
        ]
        result = deduplicate_grants(grants)
        self.assertEqual(len(result), 1)
    
    def test_find_duplicates_none(self):
        """Test finding duplicates when there are none."""
        grants = [
            {"name": "Grant A", "deadline": "4 June 2026"},
            {"name": "Grant B", "deadline": "15 July 2026"},
        ]
        result = find_duplicates(grants)
        self.assertEqual(len(result), 0)
    
    def test_find_duplicates_multiple(self):
        """Test finding multiple duplicate groups."""
        grants = [
            {"name": "Grant A", "source": "Source 1"},
            {"name": "Grant A", "source": "Source 2"},
            {"name": "Grant B", "source": "Source 1"},
            {"name": "Grant B", "source": "Source 2"},
        ]
        result = find_duplicates(grants)
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(len(result[1]), 2)


if __name__ == '__main__':
    unittest.main()
