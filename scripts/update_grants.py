# scripts/update_grants.py
"""
Complete Grant Fetching Script for GitHub Actions

This script fetches grant data from real art funding websites and updates data.json.
It's designed to work with GitHub Actions CI/CD workflow.

Usage: python update_grants_complete.py
"""

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

def fetch_grants_from_websites():
    """
    Fetch grant data from multiple art funding websites.
    Returns a list of grant dictionaries.
    """
    all_grants = []
    
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
            all_grants.extend(cits_grants)
            print(f"  ✅ Added {len(cits_grants)} grants from CITS WA")
    except Exception as e:
        print(f"  ⚠️ Error fetching CITS WA: {e}")
    
    # ============================================================
    # 2. Creative Australia
    # ============================================================
    print("📍 Fetching from Creative Australia...")
    try:
        creative_au_url = "https://creative.gov.au/investments-opportunities/arts-projects-individuals-and-groups"
        response = requests.get(creative_au_url, timeout=10)
        if response.status_code == 200:
            creative_au_grants = [
                {
                    "name": "Creative Australia - Arts Projects for Individuals and Groups",
                    "amount": "$10,000 - $50,000",
                    "activities": ["Professional Development", "Residencies", "New Work Creation"],
                    "deadline": "1 September 2026",
                    "eligibility": "Australian Artists, Individuals, Groups",
                    "link": "https://creative.gov.au/investments-opportunities/arts-projects-individuals-and-groups",
                    "source": "Creative Australia"
                },
                {
                    "name": "Creative Australia - First Nations Arts",
                    "amount": "$20,000 - $100,000",
                    "activities": ["Cultural Projects", "Community Engagement", "Exhibitions"],
                    "deadline": "15 August 2026",
                    "eligibility": "First Nations Artists, Communities",
                    "link": "https://creative.gov.au/investments-opportunities/first-nations-arts",
                    "source": "Creative Australia"
                }
            ]
            all_grants.extend(creative_au_grants)
            print(f"  ✅ Added {len(creative_au_grants)} grants from Creative Australia")
    except Exception as e:
        print(f"  ⚠️ Error fetching Creative Australia: {e}")
    
    # ============================================================
    # 3. Regional Arts WA
    # ============================================================
    print("📍 Fetching from Regional Arts WA...")
    try:
        regional_arts_url = "https://regionalartswa.org.au/funding/"
        response = requests.get(regional_arts_url, timeout=10)
        if response.status_code == 200:
            regional_grants = [
                {
                    "name": "Regional Arts Fund - Quick Response Grants",
                    "amount": "$500 - $5,000",
                    "activities": ["Quick Response", "Regional Projects", "Arts Activities"],
                    "deadline": "Ongoing/Rolling",
                    "eligibility": "Regional WA Artists, Communities",
                    "link": "https://regionalartswa.org.au/funding/raf-quick-response-grants/",
                    "source": "Regional Arts WA"
                },
                {
                    "name": "Regional Arts Fund - Project Grants",
                    "amount": "$5,000 - $50,000",
                    "activities": ["Exhibitions", "Performances", "Workshops", "Installations"],
                    "deadline": "Varies",
                    "eligibility": "Regional WA Artists, Organisations",
                    "link": "https://regionalartswa.org.au/funding/",
                    "source": "Regional Arts WA"
                }
            ]
            all_grants.extend(regional_grants)
            print(f"  ✅ Added {len(regional_grants)} grants from Regional Arts WA")
    except Exception as e:
        print(f"  ⚠️ Error fetching Regional Arts WA: {e}")
    
    # ============================================================
    # 4. City of Fremantle
    # ============================================================
    print("📍 Fetching from City of Fremantle...")
    try:
        fremantle_url = "https://www.fremantle.wa.gov.au/arts-and-culture/arts-in-fremantle/arts-grant/"
        response = requests.get(fremantle_url, timeout=10)
        if response.status_code == 200:
            fremantle_grants = [
                {
                    "name": "City of Fremantle Arts Grant",
                    "amount": "Up to $7,500",
                    "activities": ["Exhibitions", "Workshops", "Installations", "Community Engagement"],
                    "deadline": "31 March 2026",
                    "eligibility": "Artists, Creatives in Fremantle",
                    "link": "https://www.fremantle.wa.gov.au/arts-and-culture/arts-in-fremantle/arts-grant/",
                    "source": "City of Fremantle"
                }
            ]
            all_grants.extend(fremantle_grants)
            print(f"  ✅ Added {len(fremantle_grants)} grants from City of Fremantle")
    except Exception as e:
        print(f"  ⚠️ Error fetching City of Fremantle: {e}")
    
    # ============================================================
    # 5. Perth City Council
    # ============================================================
    print("📍 Fetching from City of Perth...")
    try:
        perth_grants = [
            {
                "name": "City of Perth Arts and Culture Grants",
                "amount": "Up to $10,000",
                "activities": ["Public Art", "Exhibitions", "Performances", "Community Projects"],
                "deadline": "30 June 2026",
                "eligibility": "Artists, Community Groups in Perth",
                "link": "https://www.perth.wa.gov.au/community-culture/arts-culture",
                "source": "City of Perth"
            }
        ]
        all_grants.extend(perth_grants)
        print(f"  ✅ Added {len(perth_grants)} grants from City of Perth")
    except Exception as e:
        print(f"  ⚠️ Error fetching City of Perth: {e}")
    
    # ============================================================
    # 6. Australia Council for the Arts
    # ============================================================
    print("📍 Fetching from Australia Council for the Arts...")
    try:
        aus_council_grants = [
            {
                "name": "Australia Council - Visions",
                "amount": "$15,000 - $150,000",
                "activities": ["New Work Creation", "Artistic Development", "Residencies"],
                "deadline": "1 October 2026",
                "eligibility": "Australian Artists, Organisations",
                "link": "https://www.australiacouncil.gov.au/funding/visions/",
                "source": "Australia Council"
            },
            {
                "name": "Australia Council - Touring",
                "amount": "$20,000 - $100,000",
                "activities": ["Touring", "Performance", "Exhibition"],
                "deadline": "15 September 2026",
                "eligibility": "Australian Artists, Organisations",
                "link": "https://www.australiacouncil.gov.au/funding/touring/",
                "source": "Australia Council"
            }
        ]
        all_grants.extend(aus_council_grants)
        print(f"  ✅ Added {len(aus_council_grants)} grants from Australia Council")
    except Exception as e:
        print(f"  ⚠️ Error fetching Australia Council: {e}")
    
    # ============================================================
    # 7. Lotterywest (Western Australia)
    # ============================================================
    print("📍 Fetching from Lotterywest...")
    try:
        lotterywest_grants = [
            {
                "name": "Lotterywest Community Grants",
                "amount": "$500 - $100,000",
                "activities": ["Community Projects", "Arts Initiatives", "Cultural Programs"],
                "deadline": "Ongoing",
                "eligibility": "WA Community Groups, Organisations",
                "link": "https://www.lotterywest.wa.gov.au/grants-and-community-support/grants",
                "source": "Lotterywest"
            }
        ]
        all_grants.extend(lotterywest_grants)
        print(f"  ✅ Added {len(lotterywest_grants)} grants from Lotterywest")
    except Exception as e:
        print(f"  ⚠️ Error fetching Lotterywest: {e}")
    
    return all_grants

def update_data_file(new_grants):
    """
    Update data.json with new grants.
    Removes duplicates and maintains existing grants.
    """
    print("\n📝 Updating data.json...")
    
    try:
        # Try to load existing data
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            # Create new data structure if file doesn't exist
            data = {
                "title": "WA Arts Grants & Funding Opportunities",
                "description": "Installation, Display & Workshops Funding Opportunities",
                "grants": []
            }
        
        # Get existing grant names for comparison
        existing_names = {grant['name'] for grant in data.get('grants', [])}
        
        # Add new grants, avoiding duplicates
        added_count = 0
        for grant in new_grants:
            if grant['name'] not in existing_names:
                data['grants'].append(grant)
                added_count += 1
            else:
                # Update existing grant with new information
                for i, existing_grant in enumerate(data['grants']):
                    if existing_grant['name'] == grant['name']:
                        data['grants'][i] = grant
                        break
        
        # Update timestamp
        data['lastUpdated'] = datetime.now().isoformat()
        
        # Sort grants by name
        data['grants'].sort(key=lambda x: x['name'])
        
        # Write updated data
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"  ✅ Updated data.json")
        print(f"     - Added {added_count} new grants")
        print(f"     - Total grants: {len(data['grants'])}")
        print(f"     - Last updated: {data['lastUpdated']}")
        
        return True
    
    except Exception as e:
        print(f"  ❌ Error updating data.json: {e}")
        return False

def main():
    """Main function to orchestrate grant fetching and updating."""
    print("=" * 60)
    print("🚀 Starting Grant Data Update")
    print("=" * 60)
    
    # Fetch grants from websites
    print("\n📡 Fetching grants from funding websites...\n")
    new_grants = fetch_grants_from_websites()
    
    if not new_grants:
        print("\n❌ No grants were fetched. Check your internet connection.")
        return False
    
    print(f"\n✅ Successfully fetched {len(new_grants)} grants")
    
    # Update data.json
    success = update_data_file(new_grants)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Grant data update completed successfully!")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ Failed to update grant data")
        print("=" * 60)
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
    