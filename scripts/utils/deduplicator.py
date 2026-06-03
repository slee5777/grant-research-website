"""
Grant Deduplication Module

This module provides utilities for identifying and removing duplicate grants
from the grant dataset. Duplicates can occur when the same grant is listed
by multiple funding sources or when data is updated multiple times.

The deduplication strategy prioritizes grants with later deadlines,
as these are more likely to be current.
"""

from typing import List, Dict, Any
from datetime import datetime
from .date_parser import parse_deadline


def deduplicate_grants(grants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate grants from a list, keeping the most relevant version.
    
    Duplicates are identified by matching grant names (case-insensitive).
    When duplicates are found, the version with the latest deadline is kept.
    
    Args:
        grants (List[Dict[str, Any]]): List of grant dictionaries.
    
    Returns:
        List[Dict[str, Any]]: Deduplicated list of grants.
    
    Example:
        >>> grants = [
        ...     {"name": "First Nations Arts Fund", "deadline": "15 July 2026"},
        ...     {"name": "First Nations Arts Fund", "deadline": "30 June 2026"},
        ... ]
        >>> deduplicated = deduplicate_grants(grants)
        >>> len(deduplicated)
        1
        >>> deduplicated[0]['deadline']
        '15 July 2026'
    """
    seen: Dict[str, Dict[str, Any]] = {}
    duplicates_removed = 0
    
    for grant in grants:
        # Create a normalized key for comparison (lowercase, stripped)
        key = grant.get('name', '').lower().strip()
        
        if not key:
            # Skip grants without names
            continue
        
        if key not in seen:
            # First time seeing this grant name
            seen[key] = grant
        else:
            # Duplicate found - keep the one with the later deadline
            existing_grant = seen[key]
            existing_deadline = parse_deadline(existing_grant.get('deadline', ''))
            new_deadline = parse_deadline(grant.get('deadline', ''))
            
            # Compare deadlines
            if new_deadline and (not existing_deadline or new_deadline > existing_deadline):
                seen[key] = grant
                duplicates_removed += 1
            else:
                duplicates_removed += 1
    
    if duplicates_removed > 0:
        print(f"  ℹ️ Removed {duplicates_removed} duplicate grant(s)")
    
    return list(seen.values())


def find_duplicates(grants: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """
    Find all duplicate grants in a list.
    
    Returns a list of groups, where each group contains all grants
    with the same name (case-insensitive).
    
    Args:
        grants (List[Dict[str, Any]]): List of grant dictionaries.
    
    Returns:
        List[List[Dict[str, Any]]]: List of duplicate groups.
                                    Only includes groups with 2+ grants.
    
    Example:
        >>> grants = [
        ...     {"name": "First Nations Arts Fund", "source": "Creative Australia"},
        ...     {"name": "First Nations Arts Fund", "source": "Australia Council"},
        ... ]
        >>> duplicates = find_duplicates(grants)
        >>> len(duplicates)
        1
        >>> len(duplicates[0])
        2
    """
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    
    for grant in grants:
        key = grant.get('name', '').lower().strip()
        
        if not key:
            continue
        
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(grant)
    
    # Return only groups with duplicates (2+ items)
    return [group for group in grouped.values() if len(group) > 1]


def merge_duplicate_grants(
    grant1: Dict[str, Any],
    grant2: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge two duplicate grants into a single grant entry.
    
    Combines information from both grants, with grant1 taking precedence
    for conflicting fields. Creates a list of sources if they differ.
    
    Args:
        grant1 (Dict[str, Any]): First grant dictionary.
        grant2 (Dict[str, Any]): Second grant dictionary.
    
    Returns:
        Dict[str, Any]: Merged grant dictionary.
    
    Example:
        >>> g1 = {"name": "Fund", "source": "Source A", "deadline": "15 July"}
        >>> g2 = {"name": "Fund", "source": "Source B", "deadline": "15 July"}
        >>> merged = merge_duplicate_grants(g1, g2)
        >>> merged['sources']
        ['Source A', 'Source B']
    """
    merged = grant1.copy()
    
    # Combine sources if different
    source1 = grant1.get('source', 'Unknown')
    source2 = grant2.get('source', 'Unknown')
    
    if source1 != source2:
        if 'sources' not in merged:
            merged['sources'] = [source1]
        merged['sources'].append(source2)
    
    # Use the later deadline
    deadline1 = parse_deadline(grant1.get('deadline', ''))
    deadline2 = parse_deadline(grant2.get('deadline', ''))
    
    if deadline2 and (not deadline1 or deadline2 > deadline1):
        merged['deadline'] = grant2.get('deadline', grant1.get('deadline'))
    
    return merged


def report_duplicates(grants: List[Dict[str, Any]]) -> str:
    """
    Generate a report of duplicate grants found in the list.
    
    Args:
        grants (List[Dict[str, Any]]): List of grant dictionaries.
    
    Returns:
        str: Formatted report of duplicates.
    
    Example:
        >>> grants = [...]
        >>> report = report_duplicates(grants)
        >>> print(report)
    """
    duplicates = find_duplicates(grants)
    
    if not duplicates:
        return "✅ No duplicate grants found."
    
    report = f"⚠️ Found {len(duplicates)} duplicate grant(s):\n"
    
    for group in duplicates:
        grant_name = group[0].get('name', 'Unknown')
        sources = [g.get('source', 'Unknown') for g in group]
        report += f"\n  • {grant_name}\n"
        report += f"    Sources: {', '.join(sources)}\n"
    
    return report
