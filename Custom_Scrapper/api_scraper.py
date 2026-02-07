"""
Advanced Lead Scraper with API Integrations
Uses official APIs for legitimate data collection
"""

import requests
import json
import time
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta
from config import API_KEYS, SCRAPING_CONFIG, TARGET_INDUSTRIES

logging.basicConfig(level=logging.INFO)


class APILeadScraper:
    """
    Scraper that uses legitimate APIs for data collection
    """
    
    def __init__(self):
        self.headers = {'User-Agent': SCRAPING_CONFIG['user_agent']}
        self.delay = SCRAPING_CONFIG['delay_between_requests']
    
    def scrape_apollo_io(self, filters: Dict) -> List[Dict]:
        """
        Use Apollo.io API to find companies and contacts
        Documentation: https://apolloio.github.io/apollo-api-docs/
        """
        if API_KEYS['apollo'] == 'YOUR_APOLLO_API_KEY':
            logging.warning("Apollo API key not configured")
            return []
        
        url = "https://api.apollo.io/v1/mixed_companies/search"
        
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'X-Api-Key': API_KEYS['apollo']
        }
        
        # Search for companies
        payload = {
            "page": 1,
            "per_page": 100,
            "organization_num_employees_ranges": ["10,50", "50,100", "100,250"],
            "organization_locations": ["United States"],
            "q_organization_keyword_tags": ["saas", "software", "technology"]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                companies = []
                
                for org in data.get('organizations', []):
                    company = {
                        'company_name': org.get('name'),
                        'website': org.get('website_url'),
                        'industry': org.get('industry'),
                        'employee_count': org.get('estimated_num_employees'),
                        'location': f"{org.get('city')}, {org.get('state')}",
                        'linkedin': org.get('linkedin_url'),
                        'description': org.get('short_description'),
                        'revenue': org.get('annual_revenue'),
                        'source': 'Apollo.io'
                    }
                    companies.append(company)
                
                logging.info(f"Found {len(companies)} companies from Apollo.io")
                return companies
            else:
                logging.error(f"Apollo API error: {response.status_code}")
                
        except Exception as e:
            logging.error(f"Error fetching Apollo data: {str(e)}")
        
        return []


class LinkedInScraper:
    """
    LinkedIn scraping using Proxycurl API (official LinkedIn data provider)
    Documentation: https://nubela.co/proxycurl/
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://nubela.co/proxycurl/api"
    
    def search_companies(self, keywords: List[str]) -> List[Dict]:
        """
        Search for companies on LinkedIn
        """
        url = f"{self.base_url}/search/company"
        
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        params = {
            'keywords': ' '.join(keywords),
            'type': 'STARTUP',
            'enrich_profiles': 'enrich'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json().get('results', [])
            
        except Exception as e:
            logging.error(f"LinkedIn search error: {str(e)}")
        
        return []


def main():
    """
    Example usage of API scrapers
    """
    scraper = APILeadScraper()
    
    print("🔍 Starting API-based lead generation...\n")
    
    # Example: Scrape from Apollo.io
    all_leads = []
    
    print("🚀 Fetching from Apollo.io...")
    apollo_leads = scraper.scrape_apollo_io({})
    all_leads.extend(apollo_leads)
    
    # Enrich leads with Clearbit (optional)
    if API_KEYS.get('clearbit') and API_KEYS['clearbit'] != 'YOUR_CLEARBIT_API_KEY':
        print("💎 Enriching with Clearbit...")
        for lead in all_leads[:5]:  # Enrich first 5 as example
            if lead.get('website'):
                domain = lead['website'].replace('https://', '').replace('http://', '').split('/')[0]
                enriched = scraper.enrich_with_clearbit(domain)
                lead.update(enriched)
                time.sleep(2)
    
    print(f"\n✅ Total leads collected: {len(all_leads)}")
    
    # Export to file
    with open('api_leads.json', 'w') as f:
        json.dump(all_leads, f, indent=2)
    
    print("💾 Leads saved to api_leads.json")


if __name__ == "__main__":
    main()
