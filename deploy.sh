#!/bin/bash
# Quick Deployment Script for Free Movie Searcher
# This script deploys your website to Render in one command

echo "🚀 Starting Deployment Process..."
echo ""

# Step 1: Check if we're in the correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project root directory."
    exit 1
fi

echo "✅ Project directory confirmed"
echo ""

# Step 2: Show git status
echo "📂 Current changes:"
git status --short
echo ""

# Step 3: Add all changes
echo "📦 Adding all changes to git..."
git add .
echo "✅ Files staged"
echo ""

# Step 4: Commit with timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
COMMIT_MESSAGE="Production deployment: SEO optimized + Ezoic ready - $TIMESTAMP"

echo "💾 Committing changes..."
git commit -m "$COMMIT_MESSAGE"
echo "✅ Changes committed"
echo ""

# Step 5: Push to GitHub (triggers Render auto-deploy)
echo "🚀 Pushing to GitHub..."
echo "   This will trigger automatic deployment on Render..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "📡 Render is now building and deploying..."
    echo "   This usually takes 2-5 minutes"
    echo ""
    echo "🌐 Your website will be live at:"
    echo "   https://freemoviesearcher.tech"
    echo ""
    echo "📊 Monitor deployment:"
    echo "   https://dashboard.render.com/"
    echo ""
    echo "✅ Next Steps:"
    echo "   1. Wait 5 minutes for deployment to complete"
    echo "   2. Visit https://freemoviesearcher.tech to verify"
    echo "   3. Check all pages load correctly"
    echo "   4. Verify sitemap: /sitemap.xml"
    echo "   5. Verify ads.txt: /ads.txt"
    echo "   6. Go to Google Search Console and submit sitemap"
    echo ""
    echo "📚 Full guide: See EZOIC_MONETIZATION_GUIDE.md"
    echo ""
else
    echo ""
    echo "❌ Error: Failed to push to GitHub"
    echo "   Please check your internet connection and try again"
    exit 1
fi
