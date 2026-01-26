# CI/CD Setup Instructions

## Overview
The GitHub Actions workflow automatically:
1. **Tests** the backend and frontend on every push/PR
2. **Deploys** to Render only when tests pass on the `main` branch

## Setup Steps

### 1. Get Render Deploy Hook URL

1. Go to your Render Dashboard
2. Select your `portfolio-collinearity-analyzer` service
3. Navigate to **Settings** → **Deploy Hook**
4. Copy the Deploy Hook URL (it looks like: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy`)

### 2. Add GitHub Secret

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `RENDER_DEPLOY_HOOK_URL`
5. Value: Paste the Deploy Hook URL from Render
6. Click **Add secret**

### 3. Test the Pipeline

1. Make a small change (e.g., update README)
2. Commit and push to `main`:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push origin main
   ```
3. Go to **Actions** tab in GitHub to watch the workflow run

## Workflow Behavior

- **Pull Requests**: Runs tests only (no deployment)
- **Push to main**: Runs tests → If pass, deploys to Render
- **Other branches**: No action

## Troubleshooting

If deployment fails:
- Verify the `RENDER_DEPLOY_HOOK_URL` secret is set correctly
- Check that `autoDeploy: false` in `render.yaml`
- Review the Actions logs in GitHub
