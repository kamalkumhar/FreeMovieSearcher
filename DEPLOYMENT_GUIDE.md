# 🚀 Render Deployment Guide - freemoviesearcher.tech

## ✅ Pre-Deployment Checklist

- [x] Domain: `freemoviesearcher.tech` configured
- [x] Python: 3.11 (Render default)
- [x] Server: Gunicorn (production-ready)
- [x] Files: robots.txt, sitemap.xml, ads.txt ready
- [x] SEO: All meta tags, canonical URLs set
- [x] Security: HTTPS redirects, security headers configured

---

# 📦 Step 1: Push to GitHub

```powershell
# Navigate to project
cd C:\Users\USER\Desktop\movue\Movie_recommender

# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Production ready: Render deployment with freemoviesearcher.tech domain"

# Push to GitHub
git push origin main
```

---

# 🌐 Step 2: Deploy on Render

## A. Create New Web Service

1. **Go to Render Dashboard**
   - URL: https://dashboard.render.com/
   - Click: **New +** → **Web Service**

2. **Connect GitHub Repository**
   - Select: `FreeMovieSearcher` repository
   - Click: **Connect**

## B. Configure Service

### Basic Settings:
```
Name: freemoviesearcher
Region: Oregon (US West) or Frankfurt (Europe)
Branch: main
Runtime: Python 3
```

### Build & Start Commands:
```bash
Build Command: chmod +x build.sh && ./build.sh
Start Command: gunicorn app:app
```

**OR** (Simple method):
```bash
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### Instance Type:
```
Plan: Free
```

### Environment Variables:
```
PYTHON_VERSION = 3.11.0
FLASK_ENV = production
```

## C. Advanced Settings

### Health Check Path:
```
/ (homepage)
```

### Auto-Deploy:
```
✅ Enable (deploys automatically on git push)
```

---

# 🔗 Step 3: Configure Custom Domain

## A. In Render Dashboard

1. **Go to Service Settings**
   - Navigate to: Your service → **Settings** tab
   - Scroll to: **Custom Domains**

2. **Add Domain**
   - Click: **Add Custom Domain**
   - Enter: `freemoviesearcher.tech`
   - Click: **Save**

3. **Add WWW Domain** (optional):
   - Click: **Add Custom Domain**
   - Enter: `www.freemoviesearcher.tech`
   - Click: **Save**

## B. Configure DNS (Your Domain Provider)

Render will show you DNS records. Add these to your domain provider:

### Method 1: CNAME (Recommended)
```
Type: CNAME
Name: @
Value: [your-app-name].onrender.com
TTL: 3600
```

### Method 2: A Record
```
Type: A
Name: @
Value: [Render's IP address]
TTL: 3600
```

### For WWW:
```
Type: CNAME
Name: www
Value: [your-app-name].onrender.com
TTL: 3600
```

**Wait 10-60 minutes for DNS propagation**

---

# 📊 Step 4: Verify Deployment

## A. Check Deployment Status

```
✅ Build logs show: "Build successful"
✅ Service status: "Live"
✅ Health check: Passing
```

## B. Test URLs

Open browser and test:

1. **Render URL** (temporary):
   ```
   https://freemoviesearcher.onrender.com/
   ```

2. **Custom Domain** (after DNS):
   ```
   https://freemoviesearcher.tech/
   ```

3. **Essential Files**:
   ```
   https://freemoviesearcher.tech/robots.txt
   https://freemoviesearcher.tech/sitemap.xml
   https://freemoviesearcher.tech/ads.txt
   ```

4. **Pages**:
   ```
   https://freemoviesearcher.tech/about
   https://freemoviesearcher.tech/faq
   https://freemoviesearcher.tech/contact
   ```

## C. Test Redirects

```
http://freemoviesearcher.tech/
→ Should redirect to: https://freemoviesearcher.tech/

http://www.freemoviesearcher.tech/
→ Should redirect to: https://freemoviesearcher.tech/
```

---

# 🔍 Step 5: Google Search Console Setup

## A. Add Property

1. **Go to**: https://search.google.com/search-console
2. **Click**: Add Property → Domain
3. **Enter**: `freemoviesearcher.tech`

## B. Verify Ownership

### DNS Verification (Recommended):
1. Google will give you a TXT record
2. Add to your domain's DNS:
   ```
   Type: TXT
   Name: @
   Value: google-site-verification=XXXXXXXXXXXX
   TTL: 3600
   ```
3. Wait 5-15 minutes
4. Click **Verify** in Search Console

### HTML Meta Tag (Alternative):
1. Copy verification tag from Google
2. Already added in `index.html` line 8:
   ```html
   <meta name="google-site-verification" content="YOUR_CODE_HERE">
   ```
3. Replace `YOUR_CODE_HERE` with actual code
4. Deploy changes
5. Click **Verify**

## C. Submit Sitemap

1. **In Search Console**, go to: **Sitemaps** (left menu)
2. **Enter**: `sitemap.xml`
3. **Click**: Submit
4. **Status**: Should show "Success" with 7 URLs discovered

---

# 📈 Step 6: Monitor Performance

## Render Dashboard

Check daily:
- **Metrics**: CPU, Memory usage
- **Logs**: Error monitoring
- **Uptime**: Should be 99%+

## Google Search Console

Check weekly:
- **Coverage**: Indexed pages (Week 1: 5-7, Week 4: All pages)
- **Performance**: Impressions, clicks
- **Errors**: Should be 0

---

# 🐛 Troubleshooting

## Build Failed

**Error**: `ModuleNotFoundError`
```bash
# Solution: Check requirements.txt has all dependencies
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

## 502 Bad Gateway

**Cause**: App crashed or slow to start
```bash
# Solution: Check logs in Render dashboard
# Increase timeout in render.yaml (if using)
# Or reduce ML model load time
```

## Domain Not Working

**Cause**: DNS not propagated
```bash
# Check DNS propagation
https://dnschecker.org/#CNAME/freemoviesearcher.tech

# Wait 10-60 minutes, then test again
```

## HTTPS Not Working

**Cause**: Render is provisioning SSL certificate
```
# Wait 5-15 minutes after DNS propagation
# Render automatically provides free SSL
```

---

# 📝 Important Files for Render

## render.yaml (Optional - for Blueprint)
```yaml
services:
  - type: web
    name: freemoviesearcher
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: FLASK_ENV
        value: production
```

## requirements.txt
```
flask
flask-cors
flask-compress
pandas
joblib
gunicorn
```

## build.sh (Optional)
```bash
#!/usr/bin/env bash
set -o errexit
pip install --upgrade pip
pip install -r requirements.txt
```

---

# 🎯 Post-Deployment Tasks

## Week 1:
- ✅ Test all pages and features
- ✅ Submit sitemap to Google
- ✅ Request indexing for main pages
- ✅ Set up Google Analytics (optional)

## Week 2:
- ✅ Monitor Search Console coverage
- ✅ Check for crawl errors
- ✅ Verify all pages indexed

## Week 3-4:
- ✅ Monitor traffic growth
- ✅ Track keyword rankings
- ✅ Optimize slow pages

---

# 🚨 Free Tier Limitations

## Render Free Plan:
- **Sleep after 15 mins inactivity**: First request will be slow (10-30s)
- **750 hours/month**: Enough for continuous uptime
- **100GB bandwidth/month**: Good for 10,000+ visits
- **No credit card required**: Completely free

## Solutions for Sleep:
1. Use **UptimeRobot** (free) to ping every 14 minutes
2. Upgrade to **Starter Plan** ($7/month) for no sleep

---

# ✅ Final Checklist

- [ ] Code pushed to GitHub
- [ ] Render service created and deployed
- [ ] Custom domain configured
- [ ] DNS records added
- [ ] HTTPS working
- [ ] All redirects working (www, http)
- [ ] robots.txt accessible
- [ ] sitemap.xml accessible
- [ ] Google Search Console verified
- [ ] Sitemap submitted to Google
- [ ] All pages loading correctly
- [ ] No console errors

---

# 🎉 Success!

**Your website is now LIVE at**: https://freemoviesearcher.tech

**Next**: Wait 1-4 weeks for Google to index all pages and start ranking! 🚀

---

# 📞 Support Links

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com/
- **Google Search Console**: https://search.google.com/search-console
- **DNS Checker**: https://dnschecker.org/

**Good luck with your deployment!** 🎬🍿
