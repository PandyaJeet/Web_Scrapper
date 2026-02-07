"""
Configuration file for Lead Scraper
Store your API keys and settings here
"""

# API Keys - Get these from respective platforms
API_KEYS = {
    'apollo': 'Ni3VOKHEgIDFcUPkLpBuvQ',          # https://apollo.io/ - Main lead source
    'clearbit': 'YOUR_CLEARBIT_API_KEY',      # https://clearbit.com/ - Optional for enrichment
}

# Scraping Settings
SCRAPING_CONFIG = {
    'delay_between_requests': 2,  # seconds
    'max_retries': 3,
    'timeout': 10,  # seconds
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

# Lead Scoring Weights
SCORING_WEIGHTS = {
    'funding_stage': {
        'Pre-Seed': 20,
        'Seed': 30,
        'Series A': 50,
        'Series B': 45,
        'Series C': 40,
        'Series D+': 30,
    },
    'industry_match': 30,
    'employee_count': {
        '1-10': 15,
        '10-50': 25,
        '50-100': 20,
        '100-250': 15,
        '250+': 10,
    },
    'recent_funding': 35,  # funded in last 6 months
    'website_issues': 20,
}

# Target Industries (high value for ElevatedPixels)
TARGET_INDUSTRIES = [
    'SaaS',
    'FinTech',
    'HealthTech',
    'E-commerce',
    'AI/ML',
    'EdTech',
    'PropTech',
    'Marketing Technology',
    'Enterprise Software',
    'Consumer Apps',
    'B2B Services',
    'API/Developer Tools',
]

# Target Company Sizes
TARGET_COMPANY_SIZES = [
    '10-50',
    '50-100',
    '100-250',
]

# Target Funding Stages
TARGET_FUNDING_STAGES = [
    'Seed',
    'Series A',
    'Series B',
    'Series C',
]

# Geographic Preferences
TARGET_LOCATIONS = [
    'United States',
    'Canada',
    'United Kingdom',
    'India',
    'Remote',
]

# Export Settings
EXPORT_CONFIG = {
    'default_format': 'csv',  # 'csv' or 'json'
    'include_analysis': True,
    'min_score_threshold': 50,  # only export leads with score > 50
}
