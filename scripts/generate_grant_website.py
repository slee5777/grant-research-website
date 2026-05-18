#!/usr/bin/env python3
"""
Grant Research Website Generator

This script generates an interactive HTML website from grant data.
Usage: python generate_grant_website.py <output_file> [--data data.json]
"""

import json
import sys
from pathlib import Path

def generate_html(grants_data, title="Grants & Funding Opportunities"):
    """Generate HTML website from grant data."""
    
    # Convert grants_data to list if it's a dict with 'grants' key
    if isinstance(grants_data, dict) and 'grants' in grants_data:
        grants = grants_data['grants']
        title = grants_data.get('title', title)
    else:
        grants = grants_data if isinstance(grants_data, list) else []
    
    # Build table rows
    table_rows = ""
    for grant in grants:
        activities = grant.get('activities', [])
        activity_tags = "".join([f'<span class="activity-tag">{activity}</span>' for activity in activities])
        
        table_rows += f"""
                    <tr>
                        <td class="grant-name">{grant.get('name', 'N/A')}</td>
                        <td class="amount">{grant.get('amount', 'N/A')}</td>
                        <td>{activity_tags}</td>
                        <td class="deadline">{grant.get('deadline', 'N/A')}</td>
                        <td>{grant.get('eligibility', 'N/A')}</td>
                        <td><a href="{grant.get('link', '#')}" class="link" target="_blank">View →</a></td>
                    </tr>
"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 12px; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; }}
        .header p {{ font-size: 16px; opacity: 0.9; }}
        .content {{ padding: 30px 20px; }}
        .intro {{ 
            background: #f0f4ff;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }}
        .intro h2 {{ color: #667eea; margin-bottom: 10px; font-size: 18px; }}
        .intro p {{ line-height: 1.6; color: #555; }}
        .filters {{ 
            margin-bottom: 30px; 
            display: flex; 
            gap: 10px; 
            flex-wrap: wrap;
            align-items: center;
        }}
        .filters label {{ 
            font-weight: bold; 
            color: #333;
            margin-right: 10px;
        }}
        .filters input, .filters select {{ 
            padding: 8px 12px; 
            border: 1px solid #ddd; 
            border-radius: 4px;
            font-size: 14px;
        }}
        .filters button {{ 
            padding: 8px 16px; 
            background: #667eea; 
            color: white; 
            border: none; 
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }}
        .filters button:hover {{ background: #764ba2; }}
        table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        thead {{ background: #667eea; color: white; }}
        th {{ 
            padding: 15px; 
            text-align: left; 
            font-weight: bold;
            border-bottom: 2px solid #667eea;
        }}
        td {{ 
            padding: 12px 15px; 
            border-bottom: 1px solid #eee;
        }}
        tbody tr:hover {{ background: #f9f9f9; }}
        tbody tr:nth-child(even) {{ background: #f5f5f5; }}
        .grant-name {{ font-weight: bold; color: #667eea; }}
        .amount {{ color: #27ae60; font-weight: bold; }}
        .deadline {{ color: #e74c3c; font-weight: bold; }}
        .activity-tag {{ 
            display: inline-block;
            background: #e8f0ff;
            color: #667eea;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-right: 4px;
            margin-bottom: 4px;
        }}
        .link {{ 
            color: #667eea; 
            text-decoration: none; 
            font-weight: bold;
        }}
        .link:hover {{ text-decoration: underline; }}
        .footer {{ 
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 14px;
            border-top: 1px solid #ddd;
        }}
        .no-results {{ 
            text-align: center; 
            padding: 40px; 
            color: #999;
            font-size: 16px;
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 24px; }}
            table {{ font-size: 12px; }}
            th, td {{ padding: 8px; }}
            .filters {{ flex-direction: column; align-items: flex-start; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 {title}</h1>
            <p>Funding Opportunities & Grant Resources</p>
        </div>

        <div class="content">
            <div class="intro">
                <h2>About These Grants</h2>
                <p>This comprehensive guide lists all currently available grants and funding opportunities. All grants listed below are open for applications. Use the search and filter tools to find opportunities that match your needs.</p>
            </div>

            <div class="filters">
                <label for="searchInput">Search:</label>
                <input type="text" id="searchInput" placeholder="Search by name or activity..." onkeyup="filterTable()">
                <label for="amountFilter">Min Amount:</label>
                <select id="amountFilter" onchange="filterTable()">
                    <option value="">All</option>
                    <option value="5000">$5,000+</option>
                    <option value="10000">$10,000+</option>
                    <option value="20000">$20,000+</option>
                    <option value="50000">$50,000+</option>
                </select>
                <button onclick="resetFilters()">Reset Filters</button>
            </div>

            <table id="grantsTable">
                <thead>
                    <tr>
                        <th>Grant Name</th>
                        <th>Amount</th>
                        <th>Activities Supported</th>
                        <th>Application Deadline</th>
                        <th>Eligibility</th>
                        <th>Source & Link</th>
                    </tr>
                </thead>
                <tbody>
{table_rows}
                </tbody>
            </table>

            <div id="noResults" class="no-results" style="display: none;">
                No grants match your search criteria. Try adjusting your filters.
            </div>
        </div>

        <div class="footer">
            <p><strong>Last Updated:</strong> {Path.cwd().name} | <strong>Note:</strong> Please verify deadlines and eligibility on official websites before applying.</p>
        </div>
    </div>

    <script>
        function filterTable() {{
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            const amountFilter = document.getElementById('amountFilter').value;
            const table = document.getElementById('grantsTable');
            const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
            let visibleCount = 0;

            for (let i = 0; i < rows.length; i++) {{
                const row = rows[i];
                const grantName = row.cells[0].textContent.toLowerCase();
                const activities = row.cells[2].textContent.toLowerCase();
                const amount = row.cells[1].textContent;

                let matchesSearch = grantName.includes(searchInput) || activities.includes(searchInput);
                let matchesAmount = true;

                if (amountFilter) {{
                    const amountValue = parseInt(amount.replace(/[^0-9]/g, '')) || 0;
                    matchesAmount = amountValue >= parseInt(amountFilter);
                }}

                if (matchesSearch && matchesAmount) {{
                    row.style.display = '';
                    visibleCount++;
                }} else {{
                    row.style.display = 'none';
                }}
            }}

            document.getElementById('noResults').style.display = visibleCount === 0 ? 'block' : 'none';
        }}

        function resetFilters() {{
            document.getElementById('searchInput').value = '';
            document.getElementById('amountFilter').value = '';
            const rows = document.getElementById('grantsTable').getElementsByTagName('tbody')[0].getElementsByTagName('tr');
            for (let i = 0; i < rows.length; i++) {{
                rows[i].style.display = '';
            }}
            document.getElementById('noResults').style.display = 'none';
        }}
    </script>
</body>
</html>
"""
    return html

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_grant_website.py <output_file> [--data data.json]")
        sys.exit(1)
    
    output_file = sys.argv[1]
    data_file = None
    
    # Parse optional --data argument
    if len(sys.argv) > 3 and sys.argv[2] == '--data':
        data_file = sys.argv[3]
    
    # Load grant data
    if data_file and Path(data_file).exists():
        with open(data_file, 'r') as f:
            grants_data = json.load(f)
    else:
        # Default empty structure
        grants_data = {"title": "Grants & Funding Opportunities", "grants": []}
    
    # Generate HTML
    html_content = generate_html(grants_data)
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ Website generated: {output_file}")

if __name__ == '__main__':
    main()
