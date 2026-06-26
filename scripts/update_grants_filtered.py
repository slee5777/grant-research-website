#!/usr/bin/env python3

# Copyright (c) 2026 [Assisted Evolution Pty Ltd]
# Licensed under MIT License (see LICENSE file)
# or Commercial License (see LICENSE.COMMERCIAL file)

"""
Grant Data Update Script with Deadline Filtering

This script fetches grant data from configured funding sources and filters
out grants with deadlines that have already passed. It updates the data.json
file with current, open grants only.

The script is designed to work with GitHub Actions CI/CD workflows and can
be run manually or on a schedule.

Usage:
    python update_grants_filtered.py

Environment:
    - Requires config/grants_sources.json for grant definitions
    - Outputs to data/data.json (or data.json if data/ doesn't exist)
    - Logs filtering results to stdout

Exit Codes:
    0: Success
    1: Error occurred (missing config, invalid data, etc.)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.config_loader import ConfigLoader
from utils.date_parser import parse_deadline, is_deadline_open
from utils.deduplicator import deduplicate_grants, report_duplicates


def filter_grants_by_deadline(
    grants: List[Dict[str, Any]],
    run_date: datetime = None
) -> List[Dict[str, Any]]:
    """
    Filter grants to include only those with open deadlines.
    
    Args:
        grants (List[Dict[str, Any]]): List of all grants to filter.
        run_date (datetime): Reference date for filtering.
                            Defaults to current date/time.
    
    Returns:
        List[Dict[str, Any]]: Filtered list of grants with open deadlines.
    
    Prints:
        Status messages for each grant (✅ open, ❌ closed).
    """
    if run_date is None:
        run_date = datetime.now()
    
    filtered_grants = []
    
    for grant in grants:
        deadline = grant.get('deadline', '')
        is_open = is_deadline_open(deadline, run_date)
        
        # Include if: rolling deadline (None), open (True), or unparseable (None)
        if is_open is None or is_open:
            filtered_grants.append(grant)
            print(f"  ✅ {grant.get('name', 'Unknown')} - Deadline: {deadline}")
        else:
            print(f"  ❌ {grant.get('name', 'Unknown')} - CLOSED (Deadline: {deadline})")
    
    return filtered_grants


def fetch_grants_from_config() -> List[Dict[str, Any]]:
    """
    Fetch all grants from the configuration file.
    
    Loads grants from config/grants_sources.json, organized by funding source.
    
    Returns:
        List[Dict[str, Any]]: List of all grants with source information.
    
    Raises:
        FileNotFoundError: If configuration file is missing.
        json.JSONDecodeError: If configuration file is invalid JSON.
    """
    try:
        loader = ConfigLoader()
        all_grants = loader.get_all_grants()
        return all_grants
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing configuration: {e}")
        raise


def save_grants_to_json(
    grants: List[Dict[str, Any]],
    output_file: str = 'data.json'
) -> bool:
    """
    Save grants to a JSON file.
    
    Args:
        grants (List[Dict[str, Any]]): List of grants to save.
        output_file (str): Path to output JSON file.
                          Defaults to 'data.json'.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Create output directory if it doesn't exist
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save as JSON array (not wrapped in object)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(grants, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully saved {len(grants)} grants to {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving grants to {output_file}: {e}")
        return False


def main() -> int:
    """
    Main execution function.
    
    Orchestrates the grant fetching, filtering, deduplication, and saving process.
    
    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    print("\n🚀 Starting Grant Update with Deadline Filtering")
    print(f"⏰ Run Date: {datetime.now().strftime('%d %B %Y at %H:%M:%S UTC')}\n")
    
    try:
        # Step 1: Load grants from configuration
        print("📍 Loading grants from configuration...")
        print("=" * 70)
        all_grants = fetch_grants_from_config()
        print(f"✅ Loaded {len(all_grants)} total grants from configuration\n")
        
        # Step 2: Filter by deadline
        print("📍 Filtering grants by deadline...")
        print("=" * 70)
        run_date = datetime.now()
        print(f"🔍 Filtering grants with deadlines after {run_date.strftime('%d %B %Y')}\n")
        
        filtered_grants = filter_grants_by_deadline(all_grants, run_date)
        print(f"\n✅ {len(filtered_grants)} grants have open deadlines\n")
        
        # Step 3: Deduplicate grants
        print("📍 Checking for duplicate grants...")
        print("=" * 70)
        print(report_duplicates(filtered_grants))
        deduplicated_grants = deduplicate_grants(filtered_grants)
        print(f"✅ Final count: {len(deduplicated_grants)} unique grants\n")
        
        # Step 4: Save to JSON
        print("📍 Saving grants to file...")
        print("=" * 70)
        
        # Determine output file path
        data_dir = Path('data')
        if data_dir.exists():
            output_file = 'data/data.json'
        else:
            output_file = 'data.json'
        
        success = save_grants_to_json(deduplicated_grants, output_file)
        
        if not success:
            return 1
        
        print("\n" + "=" * 70)
        print("✨ Grant update complete!")
        print("=" * 70 + "\n")
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
