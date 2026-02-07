# ElevatedPixels Lead Generation Tool

A comprehensive Python-based lead scraper designed to find potential customers for web development services.

## 🎯 What This Tool Does

This tool helps you identify and qualify leads based on your ideal customer profile:
- **Startups** that recently raised funding (Seed to Series C)
- **Companies** in high-value industries (SaaS, FinTech, HealthTech, etc.)
- **Businesses** with 10-250 employees
- **Organizations** with outdated websites or technical issues

## 📋 Features

### Core Capabilities
- ✅ Multi-source lead generation (Crunchbase, Apollo.io, Google Places, etc.)
- ✅ Website analysis (speed, mobile responsiveness, tech stack detection)
- ✅ Lead scoring based on ideal customer profile
- ✅ Email finding and contact enrichment
- ✅ Export to CSV/JSON formats
- ✅ Automated filtering and prioritization

### Data Sources Supported
1. **Apollo.io** - B2B contact database (PRIMARY SOURCE)
2. **Clearbit** - Company enrichment (OPTIONAL)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- API keys for various services (see Setup section)

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure API keys:**
   - Open `config.py`
   - Add your API keys (see API Keys section below)

4. **Run the scraper:**
```bash
python lead_scraper.py
```

## 🔑 API Keys Setup

### Required API (for full functionality)

#### Apollo.io API
- **Purpose:** Find companies and decision-makers (PRIMARY SOURCE)
- **Get API key:** https://apollo.io/
- **Cost:** Free tier available (50 credits/month)
- **Priority:** HIGH - Your main lead source
- **Steps:**
  1. Sign up at https://apollo.io/
  2. Go to Settings → API
  3. Create a new API key
  4. Select these endpoints:
     - `api/v1/mixed_companies/search` (companies + contacts)
     - `api/v1/accounts/search` (companies)
     - `api/v1/people/match` (decision-makers)

### Optional API

#### Clearbit API
- **Purpose:** Enrich company data (tech stack, revenue, employees)
- **Get API key:** https://clearbit.com/
- **Cost:** Contact for pricing
- **Priority:** LOW - Nice to have, not essential

## 📊 Usage Examples

### Basic Usage (with sample data)

```python
from lead_scraper import LeadScraper

scraper = LeadScraper()
results = scraper.run(include_website_analysis=False)

print(f"Found {results['total_leads']} leads")
print(f"High-quality leads: {results['high_quality_leads']}")
```

### Advanced Usage (with API integration)

```python
from api_scraper import APILeadScraper

scraper = APILeadScraper()

# Search Crunchbase for funded SaaS companies
leads = scraper.scrape_crunchbase_api({
    'categories': ['saas', 'software'],
    'funding_min': 1000000,  # $1M+
    'days_back': 180
})

# Enrich each lead
for lead in leads:
    if lead.get('website'):
        enriched = scraper.enrich_with_clearbit(lead['website'])
        emails = scraper.find_emails_hunter_io(lead['website'])
        lead.update(enriched)
        lead['contacts'] = emails
```

### Targeting Specific Industries

```python
from lead_scraper import LeadScraper

scraper = LeadScraper()

# Customize target industries in config.py
# Then run with filters
scraper.run()
```

## 🎯 Lead Scoring System

Leads are scored 0-100 based on:

| Factor | Points | Description |
|--------|--------|-------------|
| Funding Stage | 20-50 | Series A gets highest score |
| Industry Match | 30 | SaaS, FinTech, HealthTech preferred |
| Employee Count | 15-25 | Sweet spot: 10-100 employees |
| Recent Funding | 35 | Funded in last 6 months |
| Website Issues | 20 | Slow load, no mobile, outdated tech |

**Threshold:** Leads with score > 50 are considered high-quality

## 📁 Output Files

The scraper generates:

1. **leads_YYYYMMDD_HHMMSS.csv** - All leads with scores
2. **leads_YYYYMMDD_HHMMSS.json** - High-quality leads only (score > 50)
3. **lead_scraper.log** - Execution log

### CSV Columns

```
company_name, website, industry, funding_stage, funding_amount, 
location, employee_count, description, contact_email, linkedin, 
score, needs_redesign, load_time, source
```

## ⚙️ Configuration

Edit `config.py` to customize:

### Target Industries
```python
TARGET_INDUSTRIES = [
    'SaaS',
    'FinTech',
    'HealthTech',
    # Add more...
]
```

### Target Company Sizes
```python
TARGET_COMPANY_SIZES = [
    '10-50',
    '50-100',
    '100-250',
]
```

### Scoring Weights
```python
SCORING_WEIGHTS = {
    'funding_stage': {...},
    'industry_match': 30,
    # Customize scoring...
}
```

## 🔍 Website Analysis Features

The tool analyzes websites for:
- ✅ Load time (flags > 3 seconds)
- ✅ Mobile responsiveness (viewport meta tag)
- ✅ Outdated technology (old jQuery versions, etc.)
- ✅ Tech stack detection
- ✅ Overall redesign need score

## 💡 Best Practices

### 1. Start with Free Tiers
Begin with Apollo.io and Hunter.io free tiers to test the system.

### 2. Respect Rate Limits
The tool includes delays between requests. Don't modify unless necessary.

### 3. Focus on Quality
Use the scoring system to filter. 100 high-quality leads > 1000 low-quality leads.

### 4. Regular Updates
Run weekly to catch newly funded companies.

### 5. Combine Sources
Use multiple APIs for better coverage and enrichment.

## 🚨 Legal & Ethical Considerations

### ✅ DO:
- Use official APIs with proper authentication
- Respect rate limits and ToS
- Only collect publicly available data
- Use data for legitimate business purposes

### ❌ DON'T:
- Scrape websites that prohibit it in robots.txt
- Violate API terms of service
- Send unsolicited spam
- Store sensitive personal data without consent

### GDPR Compliance
If operating in EU:
- Document your data processing
- Provide opt-out mechanisms
- Secure data storage
- Honor deletion requests

## 🛠️ Troubleshooting

### "API key not configured" error
**Solution:** Add your API key to `config.py`

### No leads found
**Solution:** 
- Check API quotas
- Verify API keys are valid
- Adjust search parameters in config

### Slow execution
**Solution:**
- Reduce `include_website_analysis` to False
- Increase `delay_between_requests`
- Use fewer data sources

### Rate limit errors
**Solution:**
- Check API quotas
- Increase delays between requests
- Upgrade API plan if needed

## 📈 Advanced Features

### Custom Filters

```python
# Filter by location
scraper.filter_by_location(['San Francisco', 'New York', 'Austin'])

# Filter by funding amount
scraper.filter_by_funding_min(5000000)  # $5M+

# Filter by website performance
scraper.filter_by_load_time(3)  # > 3 seconds
```

### Batch Processing

```python
# Process multiple searches
queries = [
    {'industry': 'SaaS', 'funding': 'Series A'},
    {'industry': 'FinTech', 'funding': 'Seed'},
]

for query in queries:
    leads = scraper.search(query)
    scraper.export_leads(leads, f"leads_{query['industry']}.csv")
```

## 🔄 Automation

### Run Daily with Cron

```bash
# Run every day at 9 AM
0 9 * * * cd /path/to/scraper && python lead_scraper.py
```

### Integration with CRM

```python
# Export to your CRM
import salesforce  # or hubspot, pipedrive, etc.

leads = scraper.run()
for lead in leads['high_quality_leads']:
    crm.create_lead(lead)
```

## 📊 Sample Output

```
╔══════════════════════════════════════════════════════════╗
║         ElevatedPixels Lead Generation Tool              ║
║  Identifies potential customers for web dev services     ║
╚══════════════════════════════════════════════════════════╝

============================================================
LEAD GENERATION COMPLETE
============================================================
Total Leads Found: 47
High-Quality Leads: 23
CSV Export: leads_20250207_143022.csv
JSON Export: leads_20250207_143022.json
============================================================

Top 5 Leads by Score:
------------------------------------------------------------
1. TechFlow AI (Score: 95)
   Industry: SaaS
   Funding: Series A - $8M
   Location: San Francisco, CA
   Website: https://example-techflow.com
```

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Contact: support@elevatedpixels.app

## 📄 License

This tool is for internal use by ElevatedPixels. All rights reserved.

## 🔮 Future Enhancements

- [ ] Integration with more data sources
- [ ] Machine learning for better scoring
- [ ] Automated email outreach
- [ ] Chrome extension for manual research
- [ ] Real-time monitoring of company events
- [ ] Social media integration (Twitter, LinkedIn posts)

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Maintained by:** ElevatedPixels Team
