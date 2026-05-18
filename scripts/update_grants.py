# scripts/update_grants.py
import json
import requests
from datetime import datetime

def fetch_grants():
    """Fetch latest grants from APIs or web scraping"""
    # This would connect to grant databases
    # For now, it's a template
    grants = [
        "https://www.cits.wa.gov.au/funding/creative-industries-funding",

        "https://creative.gov.au/investments-opportunities/arts-projects-individuals-and-groups",

        "https://www.fremantle.wa.gov.au/arts-and-culture/arts-in-fremantle/arts-grant/",

        "https://regionalartswa.org.au/funding/"
        
    ]
    
    # Example: Fetch from Creative Australia API
    # Example: Scrape from government websites
    
    return grants

def update_data_file(new_grants):
    """Update data.json with new grants"""
    with open('data.json', 'r') as f:
        data = json.load(f)
    
    # Add new grants
    data['grants'].extend(new_grants)
    
    # Remove duplicates
    seen = set()
    unique_grants = []
    for grant in data['grants']:
        if grant['name'] not in seen:
            seen.add(grant['name'])
            unique_grants.append(grant)
    
    data['grants'] = unique_grants
    data['lastUpdated'] = datetime.now().isoformat()
    
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    new_grants = fetch_grants()
    update_data_file(new_grants)
    print(f"Updated with {len(new_grants)} new grants")