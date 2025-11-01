# Quick Deployment Script for Windows PowerShell
# This script deploys Free Movie Searcher to Render in one command

Write-Host "🚀 Starting Deployment Process..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if we're in the correct directory
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Error: app.py not found." -ForegroundColor Red
    Write-Host "   Please run this script from the project root directory." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Project directory confirmed" -ForegroundColor Green
Write-Host ""

# Step 2: Show git status
Write-Host "📂 Current changes:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Step 3: Add all changes
Write-Host "📦 Adding all changes to git..." -ForegroundColor Cyan
git add .
Write-Host "✅ Files staged" -ForegroundColor Green
Write-Host ""

# Step 4: Commit with timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMessage = "Production deployment: SEO optimized + Ezoic ready - $timestamp"

Write-Host "💾 Committing changes..." -ForegroundColor Cyan
git commit -m $commitMessage
Write-Host "✅ Changes committed" -ForegroundColor Green
Write-Host ""

# Step 5: Push to GitHub (triggers Render auto-deploy)
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "   This will trigger automatic deployment on Render..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📡 Render is now building and deploying..." -ForegroundColor Cyan
    Write-Host "   This usually takes 2-5 minutes" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🌐 Your website will be live at:" -ForegroundColor Cyan
    Write-Host "   https://freemoviesearcher.tech" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Monitor deployment:" -ForegroundColor Cyan
    Write-Host "   https://dashboard.render.com/" -ForegroundColor White
    Write-Host ""
    Write-Host "✅ Next Steps:" -ForegroundColor Green
    Write-Host "   1. Wait 5 minutes for deployment to complete"
    Write-Host "   2. Visit https://freemoviesearcher.tech to verify"
    Write-Host "   3. Check all pages load correctly"
    Write-Host "   4. Verify sitemap: https://freemoviesearcher.tech/sitemap.xml"
    Write-Host "   5. Verify ads.txt: https://freemoviesearcher.tech/ads.txt"
    Write-Host "   6. Go to Google Search Console and submit sitemap"
    Write-Host ""
    Write-Host "📚 Full guide: See EZOIC_MONETIZATION_GUIDE.md" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🎉 Deployment initiated successfully!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Error: Failed to push to GitHub" -ForegroundColor Red
    Write-Host "   Please check your internet connection and try again" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}
