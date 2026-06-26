#!/usr/bin/env python3

# Copyright (c) 2026 [Assisted Evolution Pty Ltd]
# Licensed under MIT License (see LICENSE file)
# or Commercial License (see LICENSE.COMMERCIAL file)

"""
Grant Website Generator

This script generates a responsive HTML website from grant data and configuration.
It creates an interactive website with search, filtering, and sorting capabilities.

The script loads:
- Grant data from data.json (or specified data file)
- Theme configuration from config/theme.json
- Filter options from config/filters.json

Usage:
    python generate_grant_website.py [output_file] [--data data_file]

Arguments:
    output_file: Path to output HTML file (default: index.html)
    --data: Path to grant data JSON file (default: data.json)

Examples:
    python generate_grant_website.py index.html --data data.json
    python generate_grant_website.py output/index.html --data data/data.json

Exit Codes:
    0: Success
    1: Error occurred (missing files, invalid data, etc.)
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.config_loader import ConfigLoader
from utils.amount_parser import extract_amount_value, format_amount


def load_grant_data(data_file: str) -> List[Dict[str, Any]]:
    """
    Load grant data from a JSON file.
    
    Args:
        data_file (str): Path to the grant data JSON file.
    
    Returns:
        List[Dict[str, Any]]: List of grant dictionaries.
    
    Raises:
        FileNotFoundError: If the data file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    data_path = Path(data_file)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Grant data file not found: {data_file}")
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Grant data must be a JSON array")
        
        return data
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in {data_file}: {e.msg}",
            e.doc,
            e.pos
        )


def generate_filter_options(grants: List[Dict[str, Any]]) -> str:
    """
    Generate dynamic filter options based on grant amounts.
    
    Extracts unique minimum amounts from grants and creates HTML options.
    
    Args:
        grants (List[Dict[str, Any]]): List of grant dictionaries.
    
    Returns:
        str: HTML option elements for amount filtering.
    """
    amounts = set()
    
    for grant in grants:
        amount_str = grant.get('amount', '')
        amount_value = extract_amount_value(amount_str)
        if amount_value > 0:
            amounts.add(amount_value)
    
    # Sort amounts and create options
    sorted_amounts = sorted(amounts)
    options = '<option value="">All Amounts</option>\n'
    
    for amount in sorted_amounts:
        options += f'                    <option value="{amount}">{format_amount(amount)}+</option>\n'
    
    return options.rstrip()


def generate_grant_rows(grants: List[Dict[str, Any]]) -> str:
    """
    Generate HTML table rows for grants.
    
    Args:
        grants (List[Dict[str, Any]]): List of grant dictionaries.
    
    Returns:
        str: HTML table rows with grant data.
    """
    rows = []
    
    for grant in grants:
        name = grant.get('name', 'Unknown')
        amount = grant.get('amount', 'N/A')
        deadline = grant.get('deadline', 'N/A')
        eligibility = grant.get('eligibility', 'N/A')
        source = grant.get('source', 'Unknown')
        link = grant.get('link', '#')
        activities = ', '.join(grant.get('activities', []))
        
        row = f'''            <tr class="grant-row" data-amount="{extract_amount_value(amount)}" data-deadline="{deadline}" data-source="{source}">
                <td class="grant-name"><a href="{link}" target="_blank" rel="noopener noreferrer">{name}</a></td>
                <td class="grant-amount">{amount}</td>
                <td class="grant-deadline">{deadline}</td>
                <td class="grant-eligibility">{eligibility}</td>
                <td class="grant-activities">{activities}</td>
                <td class="grant-source">{source}</td>
            </tr>'''
        rows.append(row)
    
    return '\n'.join(rows)


def generate_html(
    grants: List[Dict[str, Any]],
    theme: Dict[str, Any],
    title: str = "Grants & Funding Opportunities"
) -> str:
    """
    Generate complete HTML website from grant data and theme.
    
    Args:
        grants (List[Dict[str, Any]]): List of grant dictionaries.
        theme (Dict[str, Any]): Theme configuration dictionary.
        title (str): Page title. Defaults to "Grants & Funding Opportunities".
    
    Returns:
        str: Complete HTML document.
    """
    # Extract theme colors
    colors = theme['theme']['colors']
    gradient_start = colors['primary_gradient_start']
    gradient_end = colors['primary_gradient_end']
    text_primary = colors['text_primary']
    text_secondary = colors['text_secondary']
    text_muted = colors['text_muted']
    accent_success = colors['accent_success']
    accent_danger = colors['accent_danger']
    bg_light = colors['background_light']
    bg_neutral = colors['background_neutral']
    bg_hover = colors['background_hover']
    border_color = colors['border_color']
    
    # Generate dynamic content
    filter_options = generate_filter_options(grants)
    grant_rows = generate_grant_rows(grants)
    last_updated = datetime.now().strftime('%d %B %Y at %H:%M:%S UTC')
    total_grants = len(grants)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: {bg_neutral};
            color: {text_primary};
            line-height: 1.6;
        }}
        
        header {{
            background: linear-gradient(135deg, {gradient_start}, {gradient_end});
            color: white;
            padding: 60px 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 18px;
            opacity: 0.95;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .filters {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .filters h2 {{
            font-size: 18px;
            margin-bottom: 20px;
            color: {text_primary};
        }}
        
        .filter-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
        }}
        
        .filter-group label {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            color: {text_secondary};
        }}
        
        .filter-group input,
        .filter-group select {{
            padding: 10px;
            border: 1px solid {border_color};
            border-radius: 4px;
            font-size: 14px;
            background: white;
            color: {text_primary};
        }}
        
        .filter-group input:focus,
        .filter-group select:focus {{
            outline: none;
            border-color: {gradient_start};
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .filter-buttons {{
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }}
        
        button {{
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, {gradient_start}, {gradient_end});
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}
        
        .btn-secondary {{
            background: {bg_light};
            color: {text_primary};
            border: 1px solid {border_color};
        }}
        
        .btn-secondary:hover {{
            background: {bg_hover};
        }}
        
        .results-info {{
            margin-bottom: 20px;
            padding: 15px;
            background: {bg_light};
            border-radius: 4px;
            color: {text_secondary};
            font-size: 14px;
        }}
        
        .table-wrapper {{
            overflow-x: auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        thead {{
            background: {bg_light};
            border-bottom: 2px solid {border_color};
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: {text_primary};
            font-size: 14px;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid {border_color};
            font-size: 14px;
        }}
        
        tbody tr:hover {{
            background: {bg_hover};
        }}
        
        .grant-name a {{
            color: {gradient_start};
            text-decoration: none;
            font-weight: 600;
        }}
        
        .grant-name a:hover {{
            text-decoration: underline;
        }}
        
        .grant-amount {{
            color: {accent_success};
            font-weight: 600;
        }}
        
        .grant-deadline {{
            color: {accent_danger};
            font-weight: 600;
        }}
        
        .grant-source {{
            color: {text_muted};
            font-size: 13px;
        }}
        
        footer {{
            background: {text_primary};
            color: white;
            padding: 30px 20px;
            text-align: center;
            margin-top: 60px;
            font-size: 14px;
        }}
        
        footer a {{
            color: #87ceeb;
            text-decoration: none;
        }}
        
        footer a:hover {{
            text-decoration: underline;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 40px;
            color: {text_muted};
        }}
        
        .empty-state h3 {{
            font-size: 18px;
            margin-bottom: 10px;
        }}
        
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 24px;
            }}
            
            .filter-row {{
                grid-template-columns: 1fr;
            }}
            
            table {{
                font-size: 12px;
            }}
            
            td, th {{
                padding: 10px;
            }}
            
            .grant-activities {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>🎨 {title}</h1>
        <p>Discover funding opportunities for arts and creative projects</p>
    </header>
    
    <div class="container">
        <div class="filters">
            <h2>Search & Filter</h2>
            
            <div class="filter-row">
                <div class="filter-group">
                    <label for="searchInput">Search Grants</label>
                    <input type="text" id="searchInput" placeholder="Enter keyword...">
                </div>
                
                <div class="filter-group">
                    <label for="amountFilter">Minimum Amount</label>
                    <select id="amountFilter">
{filter_options}
                    </select>
                </div>
                
                <div class="filter-group">
                    <label for="sourceFilter">Funding Source</label>
                    <select id="sourceFilter">
                        <option value="">All Sources</option>
                    </select>
                </div>
            </div>
            
            <div class="filter-buttons">
                <button class="btn-primary" onclick="applyFilters()">🔍 Search & Filter</button>
                <button class="btn-secondary" onclick="clearFilters()">↺ Clear Filters</button>
            </div>
        </div>
        
        <div class="results-info">
            <span id="resultsCount">Showing {total_grants} grants</span>
        </div>
        
        <div class="table-wrapper">
            <table id="grantsTable">
                <thead>
                    <tr>
                        <th>Grant Name</th>
                        <th>Amount</th>
                        <th>Deadline</th>
                        <th>Eligibility</th>
                        <th>Activities</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>
{grant_rows}
                </tbody>
            </table>
        </div>
    </div>
    
    <footer>
        <p><strong>Last Updated:</strong> {last_updated}</p>
        <p><strong>Note:</strong> Please verify deadlines and eligibility on official websites before applying.</p>
        <p>For more information, visit the <a href="https://github.com/slee5777/grant-research-website">Grant Research Website</a> repository.</p>
    </footer>
    
    <script>
        // Populate source filter dynamically
        function initializeSourceFilter() {{
            const sources = new Set();
            document.querySelectorAll('.grant-row').forEach(row => {{
                const source = row.dataset.source;
                if (source) sources.add(source);
            }});
            
            const sourceFilter = document.getElementById('sourceFilter');
            Array.from(sources).sort().forEach(source => {{
                const option = document.createElement('option');
                option.value = source;
                option.textContent = source;
                sourceFilter.appendChild(option);
            }});
        }}
        
        // Apply filters
        function applyFilters() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const minAmount = parseInt(document.getElementById('amountFilter').value) || 0;
            const source = document.getElementById('sourceFilter').value;
            
            let visibleCount = 0;
            
            document.querySelectorAll('.grant-row').forEach(row => {{
                const name = row.querySelector('.grant-name').textContent.toLowerCase();
                const activities = row.querySelector('.grant-activities').textContent.toLowerCase();
                const eligibility = row.querySelector('.grant-eligibility').textContent.toLowerCase();
                const rowAmount = parseInt(row.dataset.amount) || 0;
                const rowSource = row.dataset.source;
                
                const matchesSearch = !searchTerm || name.includes(searchTerm) || activities.includes(searchTerm) || eligibility.includes(searchTerm);
                const matchesAmount = rowAmount >= minAmount;
                const matchesSource = !source || rowSource === source;
                
                const isVisible = matchesSearch && matchesAmount && matchesSource;
                row.style.display = isVisible ? '' : 'none';
                if (isVisible) visibleCount++;
            }});
            
            updateResultsCount(visibleCount);
        }}
        
        // Clear filters
        function clearFilters() {{
            document.getElementById('searchInput').value = '';
            document.getElementById('amountFilter').value = '';
            document.getElementById('sourceFilter').value = '';
            
            document.querySelectorAll('.grant-row').forEach(row => {{
                row.style.display = '';
            }});
            
            updateResultsCount(document.querySelectorAll('.grant-row').length);
        }}
        
        // Update results count
        function updateResultsCount(count) {{
            const total = document.querySelectorAll('.grant-row').length;
            const resultsSpan = document.getElementById('resultsCount');
            resultsSpan.textContent = count === total ? 
                `Showing ${{count}} grants` : 
                `Showing ${{count}} of ${{total}} grants`;
        }}
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {{
            initializeSourceFilter();
        }});
        
        // Allow Enter key to trigger search
        document.getElementById('searchInput').addEventListener('keypress', (e) => {{
            if (e.key === 'Enter') applyFilters();
        }});
    </script>
</body>
</html>'''
    
    return html


def main() -> int:
    """
    Main execution function.
    
    Parses arguments, loads data and configuration, generates HTML, and saves output.
    
    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description='Generate HTML website from grant data and configuration'
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        default='index.html',
        help='Output HTML file path (default: index.html)'
    )
    parser.add_argument(
        '--data',
        default='data.json',
        help='Grant data JSON file path (default: data.json)'
    )
    
    args = parser.parse_args()
    
    print("\n🚀 Starting Website Generation")
    print(f"⏰ Generated: {datetime.now().strftime('%d %B %Y at %H:%M:%S UTC')}\n")
    
    try:
        # Load grant data
        print(f"📍 Loading grant data from {args.data}...")
        grants = load_grant_data(args.data)
        print(f"✅ Loaded {len(grants)} grants\n")
        
        # Load theme configuration
        print("📍 Loading theme configuration...")
        loader = ConfigLoader()
        theme = loader.load_theme()
        print("✅ Theme loaded\n")
        
        # Generate HTML
        print("📍 Generating HTML website...")
        html_content = generate_html(grants, theme)
        
        # Save HTML
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Website saved to {args.output_file}\n")
        
        print("=" * 70)
        print("✨ Website generation complete!")
        print("=" * 70 + "\n")
        
        return 0
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
