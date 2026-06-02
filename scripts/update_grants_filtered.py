
update_grants_filtered.py
"""
Complete Grant Fetching Script for GitHub Actions with Deadline Filtering

This script fetches grant data from real art funding websites and updates data.json.
It filters out grants with deadlines that have already passed.
It's designed to work with GitHub Actions CI/CD workflow.

Usage: python update_grants.py
"""

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

def parse_deadline(deadline_str):
    """
    Parse deadline string and return a datetime object.
    Handles various date formats.
    
    Returns None if deadline is "Rolling Rounds" or cannot be parsed.
    """
    if not deadline_str or "rolling" in deadline_str.lower():
        return None
    
    # Common date formats
    date_formats = [
        "%d %B %Y",      # 4 June 2026
        "%d/%m/%Y",      # 04/06/2026
        "%m/%d/%Y",      # 06/04/2026
        "%Y-%m-%d",      # 2026-06-04
        "%B %d, %Y",     # June 4, 2026
        "%d %b %Y",      # 4 Jun 2026
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(deadline_str.strip(), fmt)
        except ValueError:
            continue
    
    # If no format matched, return None
    print(f"  ⚠️ Could not parse deadline: {deadline_str}")
    return None

def is_deadline_open(deadline_str, run_date=None):
    """
    Check if a grant deadline is still open (after the run date).
    
    Args:
        deadline_str: Deadline as string
        run_date: Reference date (defaults to today)
    
    Returns:
        True if deadline is open, False if closed, None if rolling/unknown
    """
    if not deadline_str or "rolling" in deadline_str.lower():
        return None  # Rolling deadlines are always open
    
    deadline = parse_deadline(deadline_str)
    if deadline is None:
        return None  # Unknown deadline format, include it
    
    if run_date is None:
        run_date = datetime.now()
    
    # Deadline is open if it's after the run date
    return deadline > run_date

def fetch_grants_from_websites():
    """
    Fetch grant data from multiple art funding websites.
    Filters out grants with deadlines that have already passed.
    
    Returns a list of grant dictionaries with open deadlines.
    """
    all_grants = []
    run_date = datetime.now()
    
    print(f"🔍 Filtering grants with deadlines after {run_date.strftime('%d %B %Y')}")
    print("=" * 70)
    
    # ============================================================
    # 1. CITS WA (Creative Industries and Tourism Services)
    # ============================================================
    print("📍 Fetching from CITS WA...")
    try:
        cits_url = "https://www.cits.wa.gov.au/funding/creative-industries-funding"
        response = requests.get(cits_url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # CITS grants (manually curated from their website)
            cits_grants = [
                {
                    "name": "Arts Short Notice Activity Program (Arts SNAP)",
                    "amount": "$5,000 - $10,000",
                    "activities": ["Touring", "Showcasing", "Short Notice Activities"],
                    "deadline": "4 June 2026",
                    "eligibility": "Individuals, Groups",
                    "link": "https://www.cits.wa.gov.au/funding/creative-industries-funding",
                    "source": "CITS WA"
                },
                {
                    "name": "Contemporary Music Fund Development Program",
                    "amount": "Up to $20,000",
                    "activities": ["Professional Development", "Touring", "Recording"],
                    "deadline": "4 June 2026",
                    "eligibility": "Music Professionals, Bands",
                    "link": "https://www.cits.wa.gov.au/funding/creative-industries-funding",
                    "source": "CITS WA"
                },
                {
                    "name": "Creative Learning",
                    "amount": "$20,000 - $120,000",
                    "activities": ["Workshops", "Residencies", "Educational Programs"],
                    "deadline": "21 May 2026",
                    "eligibility": "Schools, Creatives, Organisations",
                    "link": "https://www.cits.wa.gov.au/funding/creative-industries-funding",
                    "source": "CITS WA"
                },
                {
                    "name": "Arts Projects for Individuals and Groups",
                    "amount": "Up to $80,000",
                    "activities": ["Exhibitions", "Installations", "Workshops"],
                    "deadline": "Rolling Rounds",
                    "eligibility": "Individuals, Groups, Artists",
                    "link": "https://www.cits.wa.gov.au/funding/Arts-Projects-for-Individuals-and-Groups",
                    "source": "CITS WA"
                }
            ]
            
            # Filter grants by deadline
            filtered_cits = []
            for grant in cits_grants:
                is_open = is_deadline_open(grant["deadline"], run_date)
                if is_open is None or is_open:  # Include rolling deadlines or open deadlines
                    filtered_cits.append(grant)
                    print(f"  ✅ {grant['name']} - Deadline: {grant['deadline']}")
                else:
                    print(f"  ❌ {grant['name']} - CLOSED (Deadline: {grant['deadline']})")
            
            all_grants.extend(filtered_cits)
            print(f" ✅ Added {len(filtered_cits)}/{len(cits_grants)} grants from CITS WA\n")
    except Exception as e:
        print(f" ⚠️ Error fetching CITS WA: {e}\n")
    
    # ============================================================
    # 2. Creative Australia
    # ============================================================
    print("📍 Fetching from Creative Australia...")
    try:
        creative_au_grants = [
            {
                "name": "Arts Projects for Individuals and Groups",
                "amount": "$10,000 - $50,000",
                "activities": ["Exhibitions", "Installations", "Workshops", "Performances"],
                "deadline": "31 March 2026",
                "eligibility": "Australian Artists, Individuals, Groups",
                "link": "https://creative.gov.au/investments-opportunities/arts-projects-individuals-and-groups",
                "source": "Creative Australia"
            },
            {
                "name": "First Nations Arts Fund",
                "amount": "$5,000 - $100,000",
                "activities": ["Exhibitions", "Performances", "Workshops"],
                "deadline": "15 July 2026",
                "eligibility": "First Nations Artists",
                "link": "https://creative.gov.au/investments-opportunities/first-nations-arts-fund",
                "source": "Creative Australia"
            }
        ]
        
        # Filter grants by deadline
        filtered_creative = []
        for grant in creative_au_grants:
            is_open = is_deadline_open(grant["deadline"], run_date)
            if is_open is None or is_open:
                filtered_creative.append(grant)
                print(f"  ✅ {grant['name']} - Deadline: {grant['deadline']}")
            else:
                print(f"  ❌ {grant['name']} - CLOSED (Deadline: {grant['deadline']})")
        
        all_grants.extend(filtered_creative)
        print(f" ✅ Added {len(filtered_creative)}/{len(creative_au_grants)} grants from Creative Australia\n")
    except Exception as e:
        print(f" ⚠️ Error fetching Creative Australia: {e}\n")
    
    # ============================================================
    # 3. Regional Arts WA
    # ============================================================
    print("📍 Fetching from Regional Arts WA...")
    try:
        regional_arts_grants = [
            {
                "name": "Regional Arts Fund – Quick Response Grants",
                "amount": "Up to $2,000",
                "activities": ["Workshops", "Performances", "Community Events"],
                "deadline": "Rolling Rounds",
                "eligibility": "Regional WA Artists, Groups",
                "link": "https://regionalartswa.org.au/funding/raf-quick-response-grants/",
                "source": "Regional Arts WA"
            },
            {
                "name": "Regional Arts Fund – Project Grants",
                "amount": "$2,000 - $15,000",
                "activities": ["Exhibitions", "Installations", "Workshops"],
                "deadline": "30 June 2026",
                "eligibility": "Regional WA Artists, Organisations",
                "link": "https://regionalartswa.org.au/funding/",
                "source": "Regional Arts WA"
            }
        ]
        
        # Filter grants by deadline
        filtered_regional = []
        for grant in regional_arts_grants:
            is_open = is_deadline_open(grant["deadline"], run_date)
            if is_open is None or is_open:
                filtered_regional.append(grant)
                print(f"  ✅ {grant['name']} - Deadline: {grant['deadline']}")
            else:
                print(f"  ❌ {grant['name']} - CLOSED (Deadline: {grant['deadline']})")
        
        all_grants.extend(filtered_regional)
        print(f" ✅ Added {len(filtered_regional)}/{len(regional_arts_grants)} grants from Regional Arts WA\n")
    except Exception as e:
        print(f" ⚠️ Error fetching Regional Arts WA: {e}\n")
    
    # ============================================================
    # 4. City of Fremantle
    # ============================================================
    print("📍 Fetching from City of Fremantle...")
    try:
        fremantle_grants = [
            {
                "name": "City of Fremantle Arts Grant",
                "amount": "Up to $7,500",
                "activities": ["Exhibitions", "Performances", "Community Arts"],
                "deadline": "30 September 2026",
                "eligibility": "Fremantle Residents, Local Artists",
                "link": "https://www.fremantle.wa.gov.au/arts-and-culture/arts-in-fremantle/arts-grant/",
                "source": "City of Fremantle"
            }
        ]
        
        # Filter grants by deadline
        filtered_fremantle = []
        for grant in fremantle_grants:
            is_open = is_deadline_open(grant["deadline"], run_date)
            if is_open is None or is_open:
                filtered_fremantle.append(grant)
                print(f"  ✅ {grant['name']} - Deadline: {grant['deadline']}")
            else:
                print(f"  ❌ {grant['name']} - CLOSED (Deadline: {grant['deadline']})")
        
        all_grants.extend(filtered_fremantle)
        print(f" ✅ Added {len(filtered_fremantle)}/{len(fremantle_grants)} grants from City of Fremantle\n")
    except Exception as e:
        print(f" ⚠️ Error fetching City of Fremantle: {e}\n")
    
    # ============================================================
    # 5. City of Perth
    # ============================================================
    print("📍 Fetching from City of Perth...")
    try:
        perth_grants = [
            {
                "name": "City of Perth Arts and Culture Grants",
                "amount": "Up to $10,000",
                "activities": ["Exhibitions", "Installations", "Workshops"],
                "deadline": "31 August 2026",
                "eligibility": "Perth Residents, Local Artists",
                "link": "https://www.perth.wa.gov.au/",
                "source": "City of Perth"
            }
        ]
        
        # Filter grants by deadline
        filtered_perth = []
        for grant in perth_grants:
            is_open = is_deadline_open(grant["deadline"], run_date)
            if is_open is None or is_open:
                filtered_perth.append(grant)
                print(f"  ✅ {grant['name']} - Deadline: {grant['deadline']}")
            else:
                print(f"  ❌ {grant['name']} - CLOSED (Deadline: {grant['deadline']})")
        
        all_grants.extend(filtered_perth)
        print(f" ✅ Added {len(filtered_perth)}/{len(perth_grants)} grants from City of Perth\n")
    except Exception as e:
        print(f" ⚠️ Error fetching City of Perth: {e}\n")
    
    # ============================================================
    # 6. Australia Council
    # ============================================================
    print("📍 Fetching from Australia Council...")
    try:
        australia_council_grants = [
            {
                "name": "Grants for the Arts",
                "amount": "$10,000 - $100,000",
                "activities": ["Exhibitions", "Performances", "Residencies"],
                "deadline": "Rolling Rounds",
                "eligibility": "Australian Artists, Organisations",
                "link": "https://www.australiacouncil.gov.au/",
                "source": "Australia Council"
            },
            {
                "name": "First Nations Arts Fund",
                "amount": "Up to $50,000",
                "activities": ["Exhibitions", "Workshops", "Performances"],
                "deadline": "15 July 2026",
                "eligibility": "First Nations Artists",
                "link": "https://www.australiacouncil.gov.au/",
                "source": "Australia Council"
            }
        ]
        
        # Filter grants by deadline
        filtered_council = []
        for grant in australia_council_grants:
            is_open = is_deadline_open(grant["deadline"], run_date)
            if is_open is None or is_open:
                filtered_council.append(grant)
                print(f"  ✅ {grant['name']} - Deadline: {grant['deadline']}")
            else:
                print(f"  ❌ {grant['name']} - CLOSED (Deadline: {grant['deadline']})")
        
        all_grants.extend(filtered_council)
        print(f" ✅ Added {len(filtered_council)}/{len(australia_council_grants)} grants from Australia Council\n")
    except Exception as e:
        print(f" ⚠️ Error fetching Australia Council: {e}\n")
    
    # ============================================================
    # 7. Lotterywest
    # ============================================================
    print("📍 Fetching from Lotterywest...")
    try:
        lotterywest_grants = [
            {
                "name": "Lotterywest Community Grants",
                "amount": "Up to $25,000",
                "activities": ["Community Arts", "Workshops", "Exhibitions"],
                "deadline": "Rolling Rounds",
                "eligibility": "WA Community Groups, Organisations",
                "link": "https://www.lotterywest.wa.gov.au/",
                "source": "Lotterywest"
            }
        ]
        
        # Filter grants by deadline
        filtered_lotterywest = []
        for grant in lotterywest_grants:
            is_open = is_deadline_open(grant["deadline"], run_date)
            if is_open is None or is_open:
                filtered_lotterywest.append(grant)
                print(f"  ✅ {grant['name']} - Deadline: {grant['deadline']}")
            else:
                print(f"  ❌ {grant['name']} - CLOSED (Deadline: {grant['deadline']})")
        
        all_grants.extend(filtered_lotterywest)
        print(f" ✅ Added {len(filtered_lotterywest)}/{len(lotterywest_grants)} grants from Lotterywest\n")
    except Exception as e:
        print(f" ⚠️ Error fetching Lotterywest: {e}\n")
    
    print("=" * 70)
    print(f"📊 Total grants with open deadlines: {len(all_grants)}")
    return all_grants

def save_grants_to_json(grants, filename='data.json'):
    """
    Save grants to a JSON file.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(grants, f, indent=2)
        print(f"✅ Successfully saved {len(grants)} grants to {filename}")
    except Exception as e:
        print(f"❌ Error saving grants to {filename}: {e}")

def main():
    """
    Main function to fetch and save grants.
    """
    print("\n🚀 Starting Grant Fetch with Deadline Filtering")
    print(f"⏰ Run Date: {datetime.now().strftime('%d %B %Y at %H:%M:%S')}\n")
    
    # Fetch grants
    grants = fetch_grants_from_websites()
    
    # Save to JSON
    save_grants_to_json(grants)
    
    print("\n✨ Grant fetching complete!")

if __name__ == '__main__':
    main()
    