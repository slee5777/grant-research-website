# Grant Research Website

A professional, automated grant research website generator for discovering and tracking funding opportunities. Built with Python, featuring deadline filtering, dynamic search, and responsive design.

**Live Demo:** [View the generated website](./index.html)

---

## 🎯 Features

- **Automated Grant Updates** – Fetches and filters grants monthly via GitHub Actions
- **Deadline Filtering** – Automatically removes expired grants
- **Dynamic Search & Filter** – Search by name, amount, source, and eligibility
- **Responsive Design** – Works on desktop, tablet, and mobile devices
- **Deduplication** – Removes duplicate grants from multiple sources
- **Configurable** – Separate configuration files for grants, theme, and filters
- **Well-Tested** – Comprehensive unit tests for all utilities
- **Professional Styling** – Beautiful gradient design with accessibility in mind

---

## 📁 Project Structure

```
grant-research-website/

config/                    # Configurable data
├── grants_sources.json   # All grants (no hardcoding)
├── theme.json            # Colors and styling
└── filters.json          # Filter options

data/                    # data folder
├── data.json            # latest data file saved here

scripts/                   # Well-documented Python
├── update_grants_filtered.py    # Fetch & filter (with docstrings)
├── generate_grant_website.py    # Generate HTML (with docstrings)
└── utils/                       # Reusable utilities
    ├── __init__.py
    ├── config_loader.py
    ├── date_parser.py
    ├── amount_parser.py
    └── deduplicator.py

tests/                     # Comprehensive test suite
└── test_utilities.py     # 20+ unit tests

.github/workflows/         # Automated CI/CD
└── monthly-update.yml    # Configurable schedule

├── README.md                        # This file
├── .gitignore                       # Git ignore rules
└── docs/
    ├── LICENSING.md        # This file
    ├── COMMERCIAL_FAQ.md   # FAQ for commercial users
    └── CONTRIBUTING.md     # How to contribute
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git (for version control)
- GitHub account (for automation)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/slee5777/grant-research-website.git
   cd grant-research-website
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt  # If requirements.txt exists
   # OR manually install:
   pip install requests beautifulsoup4
   ```

3. **Run the scripts manually**
   ```bash
   # Fetch and filter grants
   python scripts/update_grants_filtered.py
   
   # Generate website
   python scripts/generate_grant_website.py index.html --data data.json
   ```

4. **View the website**
   ```bash
   # Open index.html in your browser
   open index.html  # macOS
   start index.html # Windows
   xdg-open index.html # Linux
   ```

---

## 📝 Configuration

### Adding New Grants

Edit `config/grants_sources.json` to add new grants:

```json
{
  "sources": [
    {
      "id": "funding_source_id",
      "name": "Funding Source Name",
      "description": "Description of the funding source",
      "base_url": "https://example.com/grants",
      "grants": [
        {
          "name": "Grant Name",
          "amount": "$5,000 - $10,000",
          "activities": ["Activity 1", "Activity 2"],
          "deadline": "4 June 2026",
          "eligibility": "Target audience",
          "link": "https://example.com/specific-grant"
        }
      ]
    }
  ]
}
```

### Customizing Theme

Edit `config/theme.json` to change colors and styling:

```json
{
  "theme": {
    "colors": {
      "primary_gradient_start": "#667eea",
      "primary_gradient_end": "#764ba2",
      "text_primary": "#333333",
      "accent_success": "#27ae60",
      "accent_danger": "#e74c3c"
    }
  }
}
```

### Adjusting Filters

Edit `config/filters.json` to modify filter options:

```json
{
  "filters": {
    "amount_thresholds": [5000, 10000, 20000, 50000],
    "searchable_fields": ["name", "activities", "eligibility"]
  }
}
```

---

## 🔄 Automated Updates

### GitHub Actions Workflow

The project includes an automated workflow (`.github/workflows/monthly-update.yml`) that:

1. Runs on the 1st of every month at 9 AM UTC
2. Fetches grant data from `config/grants_sources.json`
3. Filters out grants with expired deadlines
4. Removes duplicate grants
5. Generates a new website
6. Commits and pushes changes to the repository

### Changing the Schedule

Edit `.github/workflows/monthly-update.yml` and modify the cron expression:

```yaml
on:
  schedule:
    - cron: '0 9 1 * *'  # 1st of month at 9 AM UTC
    # Other options:
    # - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
    # - cron: '0 9 15 * *' # 15th of month at 9 AM UTC
```

### Manual Trigger

Trigger the workflow manually from GitHub:

1. Go to **Actions** tab
2. Select **Monthly Grant Update**
3. Click **Run workflow**
4. Select **main** branch
5. Click **Run workflow**

---

## 🧪 Testing

### Run Unit Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_utilities.py -v

# Run with coverage
pip install pytest-cov
python -m pytest tests/ --cov=scripts/utils --cov-report=html
```

### Test Coverage

The test suite covers:
- Date parsing (multiple formats, edge cases)
- Amount parsing (ranges, formats, filtering)
- Grant deduplication (case-insensitive matching)
- Configuration loading (file I/O, caching)

---

## 📊 Data Format

### Grant Data Structure

```json
[
  {
    "name": "Grant Name",
    "amount": "$5,000 - $10,000",
    "activities": ["Activity 1", "Activity 2"],
    "deadline": "4 June 2026",
    "eligibility": "Target audience",
    "link": "https://example.com/grant",
    "source": "Funding Source Name",
    "source_id": "funding_source_id"
  }
]
```

### Deadline Formats Supported

- `4 June 2026` (UK format)
- `06/04/2026` (DD/MM/YYYY)
- `04/06/2026` (MM/DD/YYYY)
- `2026-06-04` (ISO format)
- `June 4, 2026` (US format)
- `4 Jun 2026` (Abbreviated)
- `Rolling Rounds` (Always open)

### Amount Formats Supported

- `$5,000`
- `Up to $50,000`
- `$5,000 - $10,000` (Range)
- `Between $10,000 and $50,000`

---

## 🛠️ Development

### Project Structure for Developers

```
scripts/
├── update_grants_filtered.py     # Main data fetching script
├── generate_grant_website.py     # Main website generation script
└── utils/
    ├── config_loader.py          # Configuration management
    ├── date_parser.py            # Date parsing utilities
    ├── amount_parser.py          # Amount parsing utilities
    └── deduplicator.py           # Deduplication logic
```

### Adding New Utilities

1. Create a new file in `scripts/utils/`
2. Add comprehensive docstrings
3. Write unit tests in `tests/`
4. Import in main scripts as needed

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Add docstrings to all modules and functions
- Write descriptive variable names

---

## 🐛 Troubleshooting

### Website not showing

- **Solution:** Wait 1-2 minutes, hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

### Changes not appearing

- **Solution:** Check GitHub Actions workflow status
- Ensure `.github/workflows/monthly-update.yml` is committed
- Verify GitHub Pages is enabled in repository settings

### 404 error

- **Solution:** Ensure `index.html` is in the repository root
- Verify repository is public
- Check GitHub Pages settings

### Script errors

- **Solution:** Ensure Python 3.11+ is installed
- Install dependencies: `pip install -r requirements.txt`
- Check file paths are correct
- Run tests to verify utilities

### Git push fails

- **Solution:** Run `git pull origin main` first
- Ensure you have write permissions
- Check branch name is correct

---

## 📚 Documentation

### Script Documentation

All scripts include comprehensive docstrings explaining:
- Purpose and usage
- Arguments and return values
- Examples
- Exit codes

View with:
```bash
python scripts/update_grants_filtered.py --help
python scripts/generate_grant_website.py --help
```

### Utility Documentation

Each utility module includes:
- Module-level docstring
- Function docstrings with examples
- Type hints for all parameters
- Return value descriptions

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Update documentation
- Follow PEP 8 style guide
- Add docstrings to all functions
- Use type hints

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🔗 Links

- **Repository:** [GitHub](https://github.com/slee5777/grant-research-website)
- **Issues:** [Report a bug](https://github.com/slee5777/grant-research-website/issues)
- **Discussions:** [Start a discussion](https://github.com/slee5777/grant-research-website/discussions)

---

## 📞 Support

For questions or issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review existing [GitHub Issues](https://github.com/slee5777/grant-research-website/issues)
3. Create a new issue with detailed information
4. Start a discussion in GitHub Discussions

---

## 🎓 Learning Resources

- [Python Documentation](https://docs.python.org/3/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**Last Updated:** 2 June 2026  
**Maintained by:** [slee5777](https://github.com/slee5777)
