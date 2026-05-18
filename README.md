# Grant Research Website


grant-research-website/
```
├── index.html           ← Your website (generated or manual)
├── data.json            ← Grant data (update monthly)
├── README.md            ← Project description
├── CHANGELOG.md         ← Track changes
├── scripts/
│   └── generate_grant_website.py  ← Website generator
└── .gitignore           ← Files to ignore
```

# Update Grant Information
### Edit data.json with new grants
`nano data.json`

### Regenerate website
`python scripts/generate_grant_website.py index.html --data data.json`

### Push to GitHub
`git add data.json index.html`
`git commit -m "Update: Added new grants for Q2 2026"`
`git push origin main`

Setup GitHub Actions (Automatic) .github/workflows/monthly-update.yml

# Troubleshooting
| Problem | Solution |
| --- | --- |
| Website not showing | Wait 1-2 minutes, hard refresh browser (Ctrl+Shift+R) |
| Changes not appearing | Check Settings → Pages is enabled, wait for rebuild |
| 404 error | Ensure index.html is in root, repository is public |
| Can't push to GitHub | Run `git pull origin main` first |
| Broken links | Test all URLs in data.json and update |

