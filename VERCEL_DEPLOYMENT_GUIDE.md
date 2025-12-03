# Vercel Deployment Guide - FreeMovieSearcher

## Domain: https://freemoviesearcher.tech

### Prerequisites
1. Vercel account (free)
2. GitHub repository connected
3. Custom domain configured

---

## Step 1: Deploy to Vercel

### A. Install Vercel CLI (Optional)
```bash
npm install -g vercel
```

### B. Deploy via GitHub (Recommended)

1. **Push to GitHub**:
```bash
git add .
git commit -m "Vercel deployment ready with custom domain"
git push origin main
```

2. **Import Project on Vercel**:
   - Visit: https://vercel.com/new
   - Click "Import Git Repository"
   - Select: `kamalkumhar/FreeMovieSearcher`
   - Click "Import"

3. **Configure Build Settings**:
   - **Framework Preset**: Other
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
   - **Install Command**: `pip install -r requirements.txt`

4. **Environment Variables** (if needed):
   - Add any API keys or secrets
   - Example: `FLASK_ENV=production`

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app will be live at: `your-project.vercel.app`

---

## Step 2: Add Custom Domain

### A. On Vercel Dashboard

1. Go to your project settings
2. Click "Domains"
3. Add domain: `freemoviesearcher.tech`
4. Add domain: `www.freemoviesearcher.tech`

### B. DNS Configuration (Your Domain Registrar)

**For Root Domain** (freemoviesearcher.tech):
```
Type: A
Name: @
Value: 76.76.19.19
TTL: 3600
```

**For WWW Subdomain** (www.freemoviesearcher.tech):
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 3600
```

**Alternative (If A record doesn't work)**:
```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
TTL: 3600
```

### C. Verify Domain
- Wait 10-20 minutes for DNS propagation
- Vercel will auto-provision SSL certificate (Let's Encrypt)
- Visit: https://freemoviesearcher.tech
- Should see ✅ "Valid Configuration"

---

## Step 3: Google Search Console Setup

### A. Add Property

1. Visit: https://search.google.com/search-console/
2. Click "Add Property"
3. Choose "Domain" method
4. Enter: `freemoviesearcher.tech`

### B. Verify Ownership

**Method 1: HTML Meta Tag** (Easiest)
1. Google gives you a meta tag like:
   ```html
   <meta name="google-site-verification" content="ABC123XYZ..." />
   ```
2. Already added in `templates/index.html` line 9
3. Replace `YOUR_VERIFICATION_CODE_HERE` with your actual code
4. Commit and push to GitHub
5. Vercel auto-deploys
6. Click "Verify" in Google Search Console

**Method 2: DNS TXT Record**
1. Google gives you TXT record
2. Add to your domain DNS:
   ```
   Type: TXT
   Name: @
   Value: google-site-verification=YOUR_CODE
   TTL: 3600
   ```
3. Wait 10-15 minutes
4. Click "Verify"

### C. Submit Sitemap

1. After verification, go to "Sitemaps" section
2. Enter: `sitemap.xml`
3. Click "Submit"
4. Google will crawl 42 URLs

### D. Request Indexing (Optional)

Use URL Inspection tool for priority pages:
- https://freemoviesearcher.tech/
- https://freemoviesearcher.tech/blog/best-netflix-movies-2025
- https://freemoviesearcher.tech/blog/top-10-movies-all-time
- https://freemoviesearcher.tech/about
- https://freemoviesearcher.tech/faq

---

## Step 4: Ezoic Setup for Ads

### A. Apply to Ezoic

**Requirements**:
- ✅ Custom domain (freemoviesearcher.tech)
- ✅ Original content (35 blog posts)
- ✅ Traffic: 1,000+ monthly visitors (apply when you reach this)
- ✅ Google AdSense approved (recommended but not mandatory)

**Application Process**:
1. Visit: https://www.ezoic.com/
2. Click "Sign Up"
3. Choose "Publisher"
4. Enter website: `https://freemoviesearcher.tech`
5. Fill application form

### B. Integration Method (Choose One)

**Option 1: Cloudflare Integration** (Recommended - Easiest)

1. **Setup Cloudflare**:
   - Visit: https://cloudflare.com
   - Add site: `freemoviesearcher.tech`
   - Update nameservers at your domain registrar

2. **Connect Ezoic**:
   - In Ezoic dashboard, choose "Cloudflare Integration"
   - Follow setup wizard
   - Ezoic automatically injects ads via Cloudflare

3. **Benefits**:
   - No code changes needed
   - Easy to enable/disable
   - Better performance with CDN

**Option 2: Name Server Integration**

1. In Ezoic dashboard, choose "Name Server Integration"
2. Ezoic provides custom nameservers
3. Update at your domain registrar:
   ```
   ns1.ezoic.com
   ns2.ezoic.com
   ```
4. Wait for DNS propagation (24-48 hours)

**Option 3: WordPress Plugin** (Not applicable - you use Flask)

### C. Ad Placement Setup

After Ezoic approval (24-48 hours):

1. **Go to Ezoic Dashboard** → Ad Tester
2. **Enable AI Ad Testing**: Let Ezoic optimize placements
3. **Ad Density**: Start with "Medium" (recommended)
4. **Ad Types**:
   - Display ads
   - Native ads
   - Video ads (optional)
   - Sticky ads (mobile)

5. **Best Performing Locations**:
   - Above fold (header area)
   - Between blog content paragraphs
   - Sidebar (desktop)
   - End of article
   - Footer

### D. Update ads.txt

Already configured in your project:
- File: `/ads.txt` (root directory)
- Ezoic will provide their Publisher ID
- Add line like:
  ```
  ezoic.com, pub-XXXXXXXXXXXXX, DIRECT
  ```

### E. Monetization Strategy

**Month 1-2**: Focus on traffic
- Publish 2-3 new blog posts per week
- Share on social media
- Build backlinks

**Month 3**: Apply to Ezoic when traffic > 1,000/month

**Month 4+**: Optimize ads
- Monitor RPM (Revenue Per Mille)
- Test different ad densities
- Enable video ads if performance good

**Expected Revenue**:
- 1,000 visitors/month: $5-10/month
- 10,000 visitors/month: $50-150/month
- 50,000 visitors/month: $250-800/month
- 100,000+ visitors/month: $500-2,000/month

---

## Step 5: Performance Optimization

### A. Vercel Settings

**Automatic Optimizations** (Already enabled):
- ✅ Global CDN
- ✅ HTTP/2
- ✅ Gzip/Brotli compression
- ✅ SSL/HTTPS
- ✅ Edge caching

**Configure Caching**:
Add to `vercel.json` (already done):
```json
"headers": [
  {
    "source": "/static/(.*)",
    "headers": [
      {
        "key": "Cache-Control",
        "value": "public, max-age=31536000, immutable"
      }
    ]
  }
]
```

### B. Monitor Performance

**Google PageSpeed Insights**:
- Visit: https://pagespeed.web.dev/
- Enter: https://freemoviesearcher.tech
- Target: 90+ mobile, 95+ desktop

**Vercel Analytics** (Optional - Free for hobby):
- Enable in project settings
- Tracks Core Web Vitals
- Real User Monitoring (RUM)

---

## Step 6: Post-Deployment Checklist

### Vercel Deployment
- [ ] Project deployed successfully
- [ ] Custom domain `freemoviesearcher.tech` added
- [ ] SSL certificate active (https://)
- [ ] All routes working correctly
- [ ] Environment variables set (if any)

### Domain Configuration
- [ ] DNS A/CNAME records configured
- [ ] WWW redirect working (www → non-www)
- [ ] HTTPS enforced (http → https redirect)
- [ ] Domain propagation complete (check https://dnschecker.org)

### Google Search Console
- [ ] Property added and verified
- [ ] Sitemap submitted (sitemap.xml)
- [ ] Index coverage monitoring enabled
- [ ] Mobile usability checked
- [ ] Core Web Vitals monitored

### SEO Verification
- [ ] All 42 URLs accessible
- [ ] Robots.txt working (/robots.txt)
- [ ] Sitemap.xml generating (/sitemap.xml)
- [ ] Meta tags on all pages
- [ ] Structured data validated (https://search.google.com/test/rich-results)
- [ ] Canonical URLs set correctly

### Ezoic Setup (When Ready)
- [ ] Traffic > 1,000 monthly visitors
- [ ] Ezoic application submitted
- [ ] Integration method chosen (Cloudflare recommended)
- [ ] Ads.txt file updated with Ezoic Publisher ID
- [ ] Ad placements configured
- [ ] Revenue tracking enabled

### Monitoring Setup
- [ ] Google Analytics tracking (optional)
- [ ] Vercel Analytics enabled (optional)
- [ ] Error tracking configured
- [ ] Performance monitoring active

---

## Timeline Expectations

### Week 1: Deployment & Setup
- Deploy to Vercel: 30 minutes
- DNS propagation: 10-30 minutes
- Google Search Console verification: 10 minutes
- Sitemap submission: 5 minutes

### Week 2-3: Indexing Begins
- Google starts crawling: 2-3 days
- First pages indexed: 7-10 days
- 20+ pages indexed: 14-21 days

### Month 2: Traffic Growth
- Organic traffic starts: 100-300 visitors/month
- 30-40 URLs indexed
- Average position: 20-40 for keywords

### Month 3: Ezoic Application
- Traffic threshold reached: 1,000+ visitors/month
- Apply to Ezoic
- Approval time: 24-48 hours
- First ad revenue: Week 1 after approval

### Month 6: Established
- Traffic: 5,000-10,000/month
- Revenue: $50-150/month
- Domain Authority: 15-25
- Page 1 rankings: 10-15 keywords

---

## Troubleshooting

### Vercel Deployment Issues

**Build fails**:
```bash
# Check requirements.txt has all dependencies
pip install -r requirements.txt

# Test locally
python app.py
```

**Routes not working**:
- Check `vercel.json` configuration
- Ensure Flask routes are defined correctly
- Check logs in Vercel dashboard

**Domain not connecting**:
- Wait 10-20 minutes for DNS propagation
- Verify DNS records at registrar
- Use https://dnschecker.org to check propagation

### Google Search Console Issues

**Verification failed**:
- Check meta tag is on homepage
- Clear browser cache
- Wait 24 hours and retry

**Sitemap errors**:
- Visit /sitemap.xml directly
- Check XML format is valid
- Ensure all URLs return 200 status

**Pages not indexing**:
- Check robots.txt allows crawling
- Use URL Inspection tool
- Request indexing manually
- Wait 2-3 weeks (indexing takes time)

### Ezoic Issues

**Application rejected**:
- Need more traffic (1,000+ monthly)
- Need more original content
- Check content quality

**Ads not showing**:
- Check integration method configured
- Clear cache
- Wait 24 hours after setup
- Check ad blocker disabled

---

## Support & Resources

**Vercel**:
- Docs: https://vercel.com/docs
- Support: https://vercel.com/support

**Google Search Console**:
- Help: https://support.google.com/webmasters

**Ezoic**:
- Support: https://support.ezoic.com
- Community: https://www.ezoic.com/community

**Your Website**:
- Live: https://freemoviesearcher.tech
- GitHub: https://github.com/kamalkumhar/FreeMovieSearcher

---

**Last Updated**: December 3, 2025  
**Status**: Ready for deployment  
**Domain**: freemoviesearcher.tech
