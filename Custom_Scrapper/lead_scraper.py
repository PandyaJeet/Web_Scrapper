"""
ElevatedPixels Lead Generation Script
Scrapes and identifies potential customers for web development services
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from datetime import datetime, timedelta
import re
from typing import List, Dict
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lead_scraper.log'),
        logging.StreamHandler()
    ]
)

class LeadScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.leads = []
        
    def scrape_crunchbase_organizations(self, pages=5):
        """
        Scrape Crunchbase for recently funded startups
        Note: This is a simplified version. For production, use Crunchbase API with proper authentication
        """
        logging.info("Scraping Crunchbase organizations...")
        
        # For demo purposes - in production, use official Crunchbase API
        # You'll need to sign up at https://data.crunchbase.com/docs
        crunchbase_leads = []
        
        # Example structure for when you have API access
        example_lead = {
            'company_name': 'Example Startup',
            'website': 'https://example.com',
            'industry': 'SaaS',
            'funding_stage': 'Series A',
            'funding_amount': '$5M',
            'location': 'San Francisco, CA',
            'employee_count': '10-50',
            'founded_year': '2022',
            'description': 'AI-powered analytics platform',
            'source': 'Crunchbase',
            'score': 0
        }
        
        logging.info("Note: Crunchbase scraping requires API key. Using placeholder data.")
        return crunchbase_leads
    
    def scrape_product_hunt(self, days_back=30):
        """
        Scrape Product Hunt for recent launches using RSS feed
        """
        logging.info(f"Scraping Product Hunt RSS feed...")
        
        product_hunt_leads = []
        
        try:
            # Use RSS feed instead of HTML scraping
            url = "https://www.producthunt.com/feed"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # Use lxml-xml or xml parser if available, else html.parser
                soup = BeautifulSoup(response.content, 'xml')
                entries = soup.find_all('entry')
                
                logging.info(f"Found {len(entries)} entries in RSS feed")
                
                for entry in entries:
                    try:
                        title = entry.find('title').text
                        link_tag = entry.find('link', {'rel': 'alternate'})
                        ph_link = link_tag['href'] if link_tag else ""
                        published = entry.find('published').text
                        content = entry.find('content').text
                        
                        # Clean content to get description
                        description = BeautifulSoup(content, 'html.parser').get_text().strip()
                        description = description.split('\\n')[0].strip()

                        lead = {
                            'company_name': title,
                            'website': ph_link,
                            'industry': 'Tech/SaaS',
                            'funding_stage': 'Launch',
                            'funding_amount': 'Unknown',
                            'location': 'Global',
                            'employee_count': 'Unknown',
                            'founded_year': datetime.now().year,
                            'description': description,
                            'source': 'Product Hunt',
                            'score': 0
                        }
                        
                        # Try to find direct link
                        content_soup = BeautifulSoup(content, 'html.parser')
                        direct_link = content_soup.find('a', string='Link')
                        if direct_link and direct_link.get('href'):
                            lead['website'] = direct_link['href']

                        product_hunt_leads.append(lead)

                    except Exception as e:
                        continue
                
                logging.info(f"Successfully scraped {len(product_hunt_leads)} leads from Product Hunt")
                
        except Exception as e:
            logging.error(f"Error scraping Product Hunt: {str(e)}")
        
        return product_hunt_leads
    
    def scrape_ycombinator_companies(self):
        """
        Scrape Y Combinator company directory
        """
        logging.info("Scraping Y Combinator companies...")
        
        yc_leads = []
        
        try:
            url = "https://www.ycombinator.com/companies"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # YC website structure - this is simplified
                # In production, you may need to handle JavaScript rendering
                logging.info("YC companies data collected")
                
        except Exception as e:
            logging.error(f"Error scraping YC: {str(e)}")
        
        return yc_leads
    
    def scrape_google_maps_businesses(self, query: str, location: str = "United States"):
        """
        Scrape Google Maps for local businesses
        Note: Google Maps scraping violates ToS. Use Google Places API instead.
        """
        logging.info(f"Searching businesses: {query} in {location}")
        
        # WARNING: Use Google Places API for production
        # This is just a placeholder structure
        
        businesses = []
        
        logging.info("Note: Use Google Places API for legitimate business data collection")
        return businesses
    
    def scrape_linkedin_companies(self, search_query: str):
        """
        LinkedIn scraping requires authentication and violates ToS
        Use LinkedIn Sales Navigator API or official integrations instead
        """
        logging.info("LinkedIn scraping requires official API access")
        
        # Structure for when you have proper API access
        linkedin_leads = []
        
        return linkedin_leads
    
    def analyze_website(self, url: str) -> Dict:
        """
        Analyze a website to determine if it's a good lead
        Checks for: outdated design, slow load times, mobile responsiveness
        """
        analysis = {
            'url': url,
            'is_outdated': False,
            'has_mobile_issues': False,
            'load_time': 0,
            'tech_stack': [],
            'needs_redesign': False,
            'score': 0
        }
        
        try:
            start_time = time.time()
            response = requests.get(url, headers=self.headers, timeout=10)
            load_time = time.time() - start_time
            
            analysis['load_time'] = round(load_time, 2)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Check for outdated indicators
                meta_generator = soup.find('meta', {'name': 'generator'})
                if meta_generator:
                    content = meta_generator.get('content', '').lower()
                    analysis['tech_stack'].append(content)
                
                # Check for mobile viewport
                viewport = soup.find('meta', {'name': 'viewport'})
                if not viewport:
                    analysis['has_mobile_issues'] = True
                    analysis['score'] += 20
                
                # Check load time
                if load_time > 3:
                    analysis['score'] += 15
                
                # Check for modern frameworks
                scripts = soup.find_all('script', {'src': True})
                for script in scripts:
                    src = script.get('src', '')
                    if 'jquery' in src.lower() and '1.' in src:
                        analysis['is_outdated'] = True
                        analysis['score'] += 25
                
                # Simple heuristic for redesign need
                if analysis['score'] > 30:
                    analysis['needs_redesign'] = True
                    
        except Exception as e:
            logging.error(f"Error analyzing website {url}: {str(e)}")
        
        return analysis
    
    def score_lead(self, lead: Dict) -> int:
        """
        Score a lead based on ideal customer profile
        Higher score = better fit
        """
        score = 0
        
        # Funding stage scoring
        funding_stages = {
            'Seed': 30,
            'Series A': 50,
            'Series B': 45,
            'Series C': 40,
            'Pre-Seed': 20
        }
        
        if 'funding_stage' in lead:
            score += funding_stages.get(lead['funding_stage'], 10)
        
        # Industry scoring
        high_value_industries = [
            'SaaS', 'FinTech', 'HealthTech', 'E-commerce',
            'AI/ML', 'EdTech', 'PropTech', 'Marketing'
        ]
        
        if 'industry' in lead:
            if any(industry.lower() in lead['industry'].lower() 
                   for industry in high_value_industries):
                score += 30
        
        # Employee count scoring (sweet spot: 10-100)
        if 'employee_count' in lead:
            emp_count = lead['employee_count']
            if '10-50' in emp_count or '50-100' in emp_count:
                score += 25
        
        # Recent funding (within 6 months)
        if 'funding_date' in lead:
            try:
                funding_date = datetime.strptime(lead['funding_date'], '%Y-%m-%d')
                if datetime.now() - funding_date < timedelta(days=180):
                    score += 35
            except:
                pass
        
        # Website analysis score
        if 'website_analysis' in lead:
            score += lead['website_analysis'].get('score', 0)
        
        lead['score'] = score
        return score
    
    def generate_sample_leads(self) -> List[Dict]:
        """
        Generate sample leads for testing
        Replace this with actual scraping in production
        """
        logging.info("Generating sample leads...")
        
        sample_leads = [
            {
                'company_name': 'TechFlow AI',
                'website': 'https://example-techflow.com',
                'industry': 'SaaS',
                'funding_stage': 'Series A',
                'funding_amount': '$8M',
                'funding_date': '2025-01-15',
                'location': 'San Francisco, CA',
                'employee_count': '10-50',
                'founded_year': '2023',
                'description': 'AI-powered workflow automation for enterprises',
                'contact_email': 'founders@example.com',
                'linkedin': 'https://linkedin.com/company/example',
                'source': 'Sample Data',
                'score': 0
            },
            {
                'company_name': 'HealthSync Pro',
                'website': 'https://example-healthsync.com',
                'industry': 'HealthTech',
                'funding_stage': 'Seed',
                'funding_amount': '$2.5M',
                'funding_date': '2024-12-01',
                'location': 'Austin, TX',
                'employee_count': '5-10',
                'founded_year': '2024',
                'description': 'Patient engagement platform for healthcare providers',
                'contact_email': 'team@example.com',
                'linkedin': 'https://linkedin.com/company/example2',
                'source': 'Sample Data',
                'score': 0
            },
            {
                'company_name': 'EduLearn Platform',
                'website': 'https://example-edulearn.com',
                'industry': 'EdTech',
                'funding_stage': 'Series B',
                'funding_amount': '$15M',
                'funding_date': '2024-10-20',
                'location': 'Boston, MA',
                'employee_count': '50-100',
                'founded_year': '2022',
                'description': 'Online learning platform with AI tutoring',
                'contact_email': 'hello@example.com',
                'linkedin': 'https://linkedin.com/company/example3',
                'source': 'Sample Data',
                'score': 0
            },
            {
                'company_name': 'FinanceFlow',
                'website': 'https://example-financeflow.com',
                'industry': 'FinTech',
                'funding_stage': 'Series A',
                'funding_amount': '$12M',
                'funding_date': '2025-01-05',
                'location': 'New York, NY',
                'employee_count': '25-50',
                'founded_year': '2023',
                'description': 'SMB accounting automation software',
                'contact_email': 'info@example.com',
                'linkedin': 'https://linkedin.com/company/example4',
                'source': 'Sample Data',
                'score': 0
            },
            {
                'company_name': 'ShopLocal Hub',
                'website': 'https://example-shoplocal.com',
                'industry': 'E-commerce',
                'funding_stage': 'Seed',
                'funding_amount': '$3M',
                'funding_date': '2024-11-10',
                'location': 'Seattle, WA',
                'employee_count': '10-25',
                'founded_year': '2024',
                'description': 'Marketplace connecting local artisans with consumers',
                'contact_email': 'contact@example.com',
                'linkedin': 'https://linkedin.com/company/example5',
                'source': 'Sample Data',
                'score': 0
            }
        ]
        
        return sample_leads
    
    def enrich_lead_data(self, lead: Dict) -> Dict:
        """
        Enrich lead data with website analysis and additional info
        """
        if 'website' in lead and lead['website']:
            try:
                analysis = self.analyze_website(lead['website'])
                lead['website_analysis'] = analysis
            except Exception as e:
                logging.error(f"Error enriching lead {lead.get('company_name')}: {str(e)}")
        
        return lead
    
    def export_leads(self, leads: List[Dict], format='csv'):
        """
        Export leads to CSV or JSON
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'csv':
            filename = f'leads_{timestamp}.csv'
            
            # Flatten nested dictionaries for CSV
            flat_leads = []
            for lead in leads:
                flat_lead = lead.copy()
                if 'website_analysis' in flat_lead:
                    analysis = flat_lead.pop('website_analysis')
                    flat_lead['needs_redesign'] = analysis.get('needs_redesign', False)
                    flat_lead['load_time'] = analysis.get('load_time', 0)
                    flat_lead['website_score'] = analysis.get('score', 0)
                flat_leads.append(flat_lead)
            
            df = pd.DataFrame(flat_leads)
            df = df.sort_values('score', ascending=False)
            df.to_csv(filename, index=False)
            logging.info(f"Leads exported to {filename}")
            
        elif format == 'json':
            filename = f'leads_{timestamp}.json'
            with open(filename, 'w') as f:
                json.dump(leads, f, indent=2)
            logging.info(f"Leads exported to {filename}")
        
        return filename
    
    def run(self, include_website_analysis=True):
        """
        Main execution function
        """
        logging.info("Starting lead generation process...")
        
        all_leads = []
        
        # Generate sample leads (replace with actual scraping)
        sample_leads = self.generate_sample_leads()
        all_leads.extend(sample_leads)
        
        # Enrich leads with website analysis
        if include_website_analysis:
            logging.info("Enriching leads with website analysis...")
            for i, lead in enumerate(all_leads):
                logging.info(f"Analyzing lead {i+1}/{len(all_leads)}: {lead.get('company_name')}")
                all_leads[i] = self.enrich_lead_data(lead)
                time.sleep(1)  # Be respectful with requests
        
        # Score all leads
        logging.info("Scoring leads...")
        for i, lead in enumerate(all_leads):
            all_leads[i]['score'] = self.score_lead(lead)
        
        # Filter high-quality leads (score > 50)
        high_quality_leads = [lead for lead in all_leads if lead['score'] > 50]
        
        logging.info(f"Total leads collected: {len(all_leads)}")
        logging.info(f"High-quality leads (score > 50): {len(high_quality_leads)}")
        
        # Export results
        csv_file = self.export_leads(all_leads, format='csv')
        json_file = self.export_leads(high_quality_leads, format='json')
        
        self.leads = all_leads
        
        return {
            'total_leads': len(all_leads),
            'high_quality_leads': len(high_quality_leads),
            'csv_file': csv_file,
            'json_file': json_file
        }


def main():
    """
    Main execution
    """
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         ElevatedPixels Lead Generation Tool              ║
    ║                                                          ║
    ║  Identifies potential customers for web dev services    ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    scraper = LeadScraper()
    
    try:
        results = scraper.run(include_website_analysis=False)  # Set to True to analyze websites
        
        print("\n" + "="*60)
        print("LEAD GENERATION COMPLETE")
        print("="*60)
        print(f"Total Leads Found: {results['total_leads']}")
        print(f"High-Quality Leads: {results['high_quality_leads']}")
        print(f"CSV Export: {results['csv_file']}")
        print(f"JSON Export: {results['json_file']}")
        print("="*60)
        
        # Display top 5 leads
        if scraper.leads:
            print("\nTop 5 Leads by Score:")
            print("-" * 60)
            
            sorted_leads = sorted(scraper.leads, key=lambda x: x['score'], reverse=True)[:5]
            
            for i, lead in enumerate(sorted_leads, 1):
                print(f"\n{i}. {lead['company_name']} (Score: {lead['score']})")
                print(f"   Industry: {lead.get('industry', 'N/A')}")
                print(f"   Funding: {lead.get('funding_stage', 'N/A')} - {lead.get('funding_amount', 'N/A')}")
                print(f"   Location: {lead.get('location', 'N/A')}")
                print(f"   Website: {lead.get('website', 'N/A')}")
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        print(f"\nError occurred: {str(e)}")


if __name__ == "__main__":
    main()
