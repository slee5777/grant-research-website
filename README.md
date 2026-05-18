# WA Art Grant Research Website

grant-research-website/
```
├── index.html           ← Your website (generated or manual)
├── data.json            ← Grant data (update monthly)
├── README.md            ← Project description
├── CHANGELOG.md         ← Track changes
├── scripts/
│   └── generate_grant_website.py  ← Website generator
├── workflows/
│   └── monthly-updte.yml  ← generate the latest data.json
└── .gitignore           ← Files to ignore

```

# Update Grant Information
### Edit data.json with new grants
run `python scripts/update_grants.py`

### Regenerate website
run `python scripts/generate_grant_website.py index.html --data data.json`

### Push to GitHub
`git add data.json index.html`
`git commit -m "Update: Added new grants for Q2 2026"`
`git push origin main`

Note: Update data.json will trigger GitHub Actions manually to update the website

Currently, this website will be updated automatically on 1st of every month.  If change schedule is required, go to `.github/workflows/monthly-update.yml` to edit `cron expression (e.g., 0 9 1 * * for 1st of month)`.  And then `Commit` changes.
Common Schedules:
0 9 1 * * - 1st of month
0 9 * * 1 - Every Monday
0 9 15 * * - 15th of month

# Troubleshooting
| Problem | Solution |
| --- | --- |
| Website not showing | Wait 1-2 minutes, hard refresh browser (Ctrl+Shift+R) |
| Changes not appearing | Check Settings → Pages is enabled, wait for rebuild |
| 404 error | Ensure index.html is in root, repository is public |
| Can't push to GitHub | Run `git pull origin main` first |
| Broken links | Test all URLs in data.json and update |
