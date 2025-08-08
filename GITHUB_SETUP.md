# Complete Guide: GitHub as Database Setup

## Overview
This guide will help you set up your loan billing system to use GitHub as a free, permanent database. All loan data will be stored as JSON files in a GitHub repository.

## Step 1: Create GitHub Repository for Data

1. **Go to GitHub.com** and sign in to your account
2. **Create a new repository:**
   - Click the "+" icon → "New repository"
   - Name it: `loan-data` (or any name you prefer)
   - Make it **Public** (required for free API access)
   - Don't initialize with README
   - Click "Create repository"

## Step 2: Create GitHub Personal Access Token

1. **Go to GitHub Settings:**
   - Click your profile picture → "Settings"
   - Scroll down to "Developer settings" (bottom left)
   - Click "Personal access tokens" → "Tokens (classic)"

2. **Generate new token:**
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a name: "Loan Billing System"
   - Set expiration: "No expiration" (or 90 days)
   - Select scopes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `public_repo` (Access public repositories)
   - Click "Generate token"

3. **Copy the token** (you won't see it again!)

## Step 3: Set Up Environment Variables on Render

1. **Go to your Render service dashboard**
2. **Click "Environment" tab**
3. **Add these environment variables:**

```
GITHUB_USERNAME=your_github_username
GITHUB_REPO=loan-data
GITHUB_TOKEN=your_personal_access_token
```

Replace:
- `your_github_username` with your actual GitHub username
- `loan-data` with your repository name
- `your_personal_access_token` with the token you copied

## Step 4: Deploy Your App

1. **Push your code to GitHub**
2. **Render will automatically redeploy**
3. **Your app will now use GitHub as the database!**

## How It Works

- **Data Storage:** All loans are stored in `loans.json` file in your GitHub repository
- **API Access:** Your app uses GitHub API to read/write data
- **Permanent:** Data survives service restarts and is version controlled
- **Free:** No database costs, completely free storage

## Benefits

✅ **Completely free** - No database costs  
✅ **Permanent storage** - Data survives restarts  
✅ **Version control** - All changes are tracked  
✅ **Backup included** - GitHub automatically backs up your data  
✅ **No setup fees** - 100% free forever  

## File Structure in GitHub

Your repository will contain:
```
loan-data/
└── loans.json  # All loan data in JSON format
```

## Example loans.json
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "description": "Home renovation loan",
    "date": "2024-01-15",
    "amount": 5000.00,
    "status": "Unpaid",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

## Troubleshooting

### If you get "Not Found" errors:
- Make sure your repository is **public**
- Check that your GitHub username and repository name are correct
- Verify your personal access token has the correct permissions

### If you get "Rate limit" errors:
- GitHub has API rate limits for free accounts
- This is usually not an issue for small applications
- If needed, you can upgrade to a paid GitHub plan

### If data doesn't save:
- Check your environment variables on Render
- Make sure your GitHub token is valid
- Check the Render logs for error messages

## Security Notes

- Your repository will be public (required for free API access)
- Only loan data will be stored (no sensitive information)
- You can make it private if you upgrade to a paid GitHub plan

## Next Steps

1. Follow the setup steps above
2. Deploy your app
3. Test adding, editing, and deleting loans
4. Your data will now be permanently stored in GitHub!

---

**Your loan billing system will now have permanent, free data storage using GitHub!** 🎉 