# WA Art Grant Research Website

# Update Grant Information by triggering Git Actions

1. Go to GitHub repository
2. Click "Actions" tab
3. Click "Monthly Update" (or your workflow name)
4. Click "Run workflow" button
5. Select "main" branch
6. Click "Run workflow"

# Alternatively, Update Grant Information
### Edit data.json with new grants
run `python scripts/update_grants_filtered.py`

### Regenerate website
run `python scripts/generate_grant_website.py index.html --data data.json`

### Push to GitHub
```python
git add data.json index.html
git commit -m "Update: Added new grants for Q2 2026"
git push origin main
```

Note: Update data.json will trigger GitHub Actions manually to update the website

Currently, this website will be updated automatically on 1st of every month.  If change schedule is required, go to `.github/workflows/monthly-update.yml` to edit `cron expression (e.g., 0 9 1 * * for 1st of month)`.  And then `Commit` changes.
```
Common Schedules:
0 9 1 * * - 1st of month
0 9 * * 1 - Every Monday
0 9 15 * * - 15th of month
```

# Troubleshooting
| Problem | Solution |
| --- | --- |
| Website not showing | Wait 1-2 minutes, hard refresh browser (Ctrl+Shift+R) |
| Changes not appearing | Check Settings → Pages is enabled, wait for rebuild |
| 404 error | Ensure index.html is in root, repository is public |
| Can't push to GitHub | Run `git pull origin main` first |
| Broken links | Test all URLs in data.json and update |


## Licensing

This project is available under two licenses:

### Community License (MIT)
For non-commercial use, education, and community projects.
See [LICENSE](LICENSE) for details.

### Commercial License
For commercial use, white-label deployments, and proprietary modifications.
Contact: [sarada@assistedevolution.net]
See [LICENSE.COMMERCIAL](LICENSE.COMMERCIAL) for details.

```json
{
  "license": "MIT OR SEE LICENSE.COMMERCIAL",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/grant-research-website"
  }
}
```