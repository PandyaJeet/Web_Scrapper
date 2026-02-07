# 🚀 QUICK START GUIDE - ElevatedPixels Lead Scraper

## Get Started in 5 Minutes

### Option 1: Use Sample Data (No Setup Required)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the pipeline
python run_pipeline.py
```

That's it! You'll get:
- ✅ 5 sample leads with scores
- ✅ Personalized outreach emails
- ✅ CSV files ready for import
- ✅ Summary report

---

### Option 2: Use Apollo.io API (Recommended for Real Leads)

#### Step 1: Get Apollo.io API Key (5 min)

1. **Sign up at Apollo.io**
   - Go to: https://apollo.io/
   - Create free account
   - **Free tier: 50 credits/month** ✨

2. **Get your API key**
   - Go to **Settings** → **API**
   - Click **"Create new key"**
   - Select these endpoints:
     - ✅ `api/v1/mixed_companies/search` (BEST - companies + contacts)
     - ✅ `api/v1/accounts/search` (companies only)
     - ✅ `api/v1/people/match` (find decision-makers)
   - Click **"Set as master key"**
   - Click **"Create API key"**
   - **Copy your API key** (you'll need this!)

#### Step 2: Configure Your API Key

Open `config.py` and paste your API key:

```python
API_KEYS = {
    'apollo': 'YOUR_APOLLO_KEY_HERE',  # ← Paste your key here
    'clearbit': 'YOUR_CLEARBIT_API_KEY',  # Optional - leave as is
}
```

#### Step 3: Enable API Mode

Open `run_pipeline.py` and change line 213:

```python
USE_APIS = True  # Change from False to True
```

#### Step 4: Run It!

```bash
python run_pipeline.py
```

---

## 📊 What You Get

### Files Generated:
1. **all_leads_TIMESTAMP.csv** - All scraped leads
2. **high_quality_leads_TIMESTAMP.json** - Leads with score > 50
3. **email_campaign_TIMESTAMP.csv** - Ready-to-send emails
4. **summary_report_TIMESTAMP.txt** - Overview and top leads

### Lead Scoring:
- **0-25**: Low quality (skip)
- **26-50**: Medium quality (consider)
- **51-75**: Good quality (contact) ⭐
- **76-100**: Excellent quality (priority) 🌟

---

## 🎯 What Apollo.io Finds For You

### ✅ Target Industries:
- SaaS companies
- FinTech startups
- HealthTech companies
- E-commerce businesses
- EdTech platforms
- AI/ML companies
- B2B software companies

### ✅ Company Criteria:
- **Size:** 10-250 employees
- **Location:** United States (customizable)
- **Type:** Growing tech companies
- **Contacts:** Founders, CEOs, CTOs, VPs

### ✅ What You Get Per Lead:
- Company name
- Website URL
- Industry
- Employee count
- Location
- Description
- LinkedIn profile
- **Decision-maker contacts** (name, title, sometimes email)

---

## 💌 Using the Outreach Emails

### Step-by-Step Process:

1. **Review Leads**
   ```bash
   # Open the CSV file
   open email_campaign_*.csv
   ```

2. **Personalize Top Leads**
   - Focus on leads with score > 70
   - Add 1-2 custom lines about their product
   - Mention something specific from their website

3. **Import to Email Tool**
   - Gmail with mail merge extension
   - Mailchimp, SendGrid, or Lemlist
   - Send in small batches (20-30/day max)

4. **Follow-Up Sequence**
   - **Day 1:** Initial email
   - **Day 3:** Follow-up #1 (if no response)
   - **Day 7:** Follow-up #2 (if no response)
   - **Day 30:** Value email (case study, blog post)

---

## 🔧 Customization

### Target Different Industries:

Edit `config.py`:
```python
TARGET_INDUSTRIES = [
    'SaaS',
    'FinTech',
    'Your Custom Industry',  # Add your industries here
]
```

### Change Company Size:

Edit `config.py`:
```python
TARGET_COMPANY_SIZES = [
    '10-50',    # Small startups
    '50-100',   # Growing companies
    '100-250',  # Established companies
]
```

### Adjust Minimum Score:

Edit `run_pipeline.py`:
```python
MIN_SCORE = 70  # Only get the best leads (default is 50)
```

---

## 📈 Expected Results

### With Sample Data:
- **Runtime:** <1 second
- **Leads:** 5 sample companies
- **Cost:** $0

### With Apollo.io Free Tier:
- **Runtime:** 2-5 minutes
- **Leads:** 50-100 companies/month
- **Cost:** $0
- **Contacts:** Founders, CTOs, decision-makers

### With Apollo.io Paid Plan ($49/mo):
- **Runtime:** 5-15 minutes
- **Leads:** 500-1000 companies/month
- **Cost:** $49/month
- **ROI:** 1-2 clients = 10-20x return 💰

---

## 🚨 Common Issues

### "Module not found" error
```bash
pip install -r requirements.txt
```

### No leads found from Apollo.io
- ✅ Check internet connection
- ✅ Verify API key is correct (no extra spaces)
- ✅ Check Apollo.io credits: Settings → API → Usage
- ✅ Try sample data first: `USE_APIS = False`

### API quota exceeded
- Check your Apollo.io dashboard
- Free tier: 50 credits/month
- Upgrade to paid plan for more credits
- Credits reset monthly

### Emails have no recipients
- Apollo.io provides contact info when available
- Not all companies have public email addresses
- Focus on LinkedIn outreach for those without emails

---

## 💡 Pro Tips

### 1. Start Small & Test
- ✅ Use sample data first to understand the output
- ✅ Run Apollo.io with 10-20 leads to test
- ✅ Review quality before scaling up

### 2. Quality Over Quantity
- Better to contact **10 perfect leads**
- Than **100 mediocre ones**
- Use score > 70 for your first batch

### 3. Track Your Results
- Which emails get responses?
- Which industries convert best?
- What subject lines work?
- Use this data to improve

### 4. Personalization is Key
```
Generic email: 5% response rate
Personalized email: 20-30% response rate
```

**Always add:**
- Something specific about their product
- Why you chose to reach out
- A clear, single call-to-action

---

## 🎯 Success Formula

```
Good Leads (Apollo.io) 
+ Personalized Emails (Your effort) 
+ Consistent Follow-up (Automation)
= New Clients 🎉
```

**Quick Wins:**
1. ✅ Run sample data (5 min)
2. ✅ Get Apollo.io free account (5 min)
3. ✅ Run first real batch (10 min)
4. ✅ Send 10 personalized emails (30 min)
5. ✅ Track results and iterate

**Don't overthink it - just start!** 🚀

---

## 📞 Next Steps

1. ✅ Test with sample data
2. ✅ Sign up for Apollo.io (free)
3. ✅ Get your API key
4. ✅ Run your first batch
5. ✅ Personalize top 10 leads
6. ✅ Send first emails
7. ✅ Track results
8. ✅ Scale what works

---

## 🆘 Need Help?

- **Full Documentation:** See `README.md`
- **API Issues:** Check Apollo.io docs at https://apolloio.github.io/apollo-api-docs/
- **Script Issues:** Review the log file: `lead_scraper.log`

---

**Version:** 2.0 (Simplified - Apollo.io Only)  
**Last Updated:** February 2026  
**Maintained by:** ElevatedPixels Team
