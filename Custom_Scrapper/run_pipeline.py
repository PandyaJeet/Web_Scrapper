"""
Complete Lead Generation Automation Pipeline
Runs the full workflow from scraping to outreach
"""

import pandas as pd
import json
from datetime import datetime
import logging
from lead_scraper import LeadScraper
from api_scraper import APILeadScraper
from email_generator import EmailOutreachGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class LeadGenerationPipeline:
    """
    Complete pipeline for lead generation and outreach
    """
    
    def __init__(self):
        self.scraper = LeadScraper()
        self.api_scraper = APILeadScraper()
        self.email_generator = EmailOutreachGenerator()
        self.all_leads = []
        
    def step1_collect_leads(self, use_apis=False):
        """
        Step 1: Collect leads from various sources
        """
        print("\n" + "="*60)
        print("STEP 1: COLLECTING LEADS")
        print("="*60)
        
        if use_apis:
            logging.info("Using Apollo.io API...")
            
            # Apollo.io - Main source
            try:
                apollo_leads = self.api_scraper.scrape_apollo_io({})
                self.all_leads.extend(apollo_leads)
                logging.info(f"✓ Apollo.io: {len(apollo_leads)} leads")
            except Exception as e:
                logging.error(f"✗ Apollo.io failed: {str(e)}")
        
        else:
            logging.info("Running manual scrapers...")
            
            # Product Hunt (RSS)
            product_hunt_leads = self.scraper.scrape_product_hunt()
            self.all_leads.extend(product_hunt_leads)
            
            # Generate sample leads as fallback/supplement
            if not product_hunt_leads:
                logging.info("No leads found from scraping, adding sample data...")
            else:
                 logging.info("Adding sample data for demonstration...")
                 
            sample_leads = self.scraper.generate_sample_leads()
            self.all_leads.extend(sample_leads)
        
        print(f"\\n📊 Total leads collected: {len(self.all_leads)}")
        return len(self.all_leads)
    
    def step2_enrich_leads(self):
        """
        Step 2: Enrich leads with additional data
        """
        print("\n" + "="*60)
        print("STEP 2: ENRICHING LEAD DATA")
        print("="*60)
        
        enriched_count = 0
        
        for i, lead in enumerate(self.all_leads):
            logging.info(f"Enriching lead {i+1}/{len(self.all_leads)}: {lead.get('company_name')}")
            
            # Website analysis
            if lead.get('website'):
                try:
                    analysis = self.scraper.analyze_website(lead['website'])
                    lead['website_analysis'] = analysis
                    enriched_count += 1
                except Exception as e:
                    logging.error(f"Website analysis failed: {str(e)}")
            
            # Company enrichment with Clearbit (if API available)
            if lead.get('website') and hasattr(self.api_scraper, 'enrich_with_clearbit'):
                try:
                    domain = lead['website'].replace('https://', '').replace('http://', '').split('/')[0]
                    enriched = self.api_scraper.enrich_with_clearbit(domain)
                    if enriched:
                        lead.update(enriched)
                except Exception as e:
                    logging.error(f"Clearbit enrichment failed: {str(e)}")
        
        print(f"\n✓ Enriched {enriched_count} leads")
        return enriched_count
    
    def step3_score_and_filter(self, min_score=50):
        """
        Step 3: Score leads and filter by quality
        """
        print("\n" + "="*60)
        print("STEP 3: SCORING AND FILTERING LEADS")
        print("="*60)
        
        # Score all leads
        for lead in self.all_leads:
            lead['score'] = self.scraper.score_lead(lead)
        
        # Filter high-quality leads
        high_quality = [lead for lead in self.all_leads if lead['score'] >= min_score]
        
        # Sort by score
        high_quality.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"\n📊 Scoring complete:")
        print(f"   Total leads: {len(self.all_leads)}")
        print(f"   High-quality (score ≥ {min_score}): {len(high_quality)}")
        print(f"   Average score: {sum(l['score'] for l in self.all_leads) / len(self.all_leads):.1f}")
        
        # Show score distribution
        score_ranges = {
            '0-25': 0,
            '26-50': 0,
            '51-75': 0,
            '76-100': 0
        }
        
        for lead in self.all_leads:
            score = lead['score']
            if score <= 25:
                score_ranges['0-25'] += 1
            elif score <= 50:
                score_ranges['26-50'] += 1
            elif score <= 75:
                score_ranges['51-75'] += 1
            else:
                score_ranges['76-100'] += 1
        
        print("\n   Score Distribution:")
        for range_name, count in score_ranges.items():
            print(f"   {range_name}: {count} leads")
        
        return high_quality
    
    def step4_generate_outreach(self, high_quality_leads):
        """
        Step 4: Generate personalized outreach emails
        """
        print("\n" + "="*60)
        print("STEP 4: GENERATING OUTREACH EMAILS")
        print("="*60)
        
        emails = []
        
        for lead in high_quality_leads:
            # Determine best template
            if lead.get('funding_stage') and lead.get('funding_date'):
                template_type = 'funded_startup'
            elif lead.get('website_analysis', {}).get('needs_redesign'):
                template_type = 'outdated_website'
            else:
                template_type = 'cold_outreach'
            
            email = self.email_generator.generate_email(lead, template_type)
            email['lead_data'] = lead
            emails.append(email)
        
        print(f"\n✓ Generated {len(emails)} personalized emails")
        
        # Show sample
        if emails:
            print("\n" + "-"*60)
            print("SAMPLE EMAIL:")
            print("-"*60)
            sample = emails[0]
            print(f"To: {sample['to']}")
            print(f"Subject: {sample['subject']}")
            print(f"\n{sample['body'][:300]}...")
        
        return emails
    
    def step5_export_results(self, high_quality_leads, emails):
        """
        Step 5: Export all results
        """
        print("\n" + "="*60)
        print("STEP 5: EXPORTING RESULTS")
        print("="*60)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. Export all leads to CSV
        leads_file = f'all_leads_{timestamp}.csv'
        flat_leads = []
        for lead in self.all_leads:
            flat = lead.copy()
            # Flatten nested dicts
            if 'website_analysis' in flat:
                analysis = flat.pop('website_analysis')
                flat['needs_redesign'] = analysis.get('needs_redesign', False)
                flat['load_time'] = analysis.get('load_time', 0)
                flat['has_mobile_issues'] = analysis.get('has_mobile_issues', False)
            if 'contacts' in flat:
                flat.pop('contacts')  # Too complex for CSV
            flat_leads.append(flat)
        
        pd.DataFrame(flat_leads).to_csv(leads_file, index=False)
        print(f"✓ All leads: {leads_file}")
        
        # 2. Export high-quality leads to JSON
        hq_file = f'high_quality_leads_{timestamp}.json'
        with open(hq_file, 'w') as f:
            json.dump(high_quality_leads, f, indent=2)
        print(f"✓ High-quality leads: {hq_file}")
        
        # 3. Export email campaign
        email_file = f'email_campaign_{timestamp}.csv'
        email_data = []
        for email in emails:
            lead = email.get('lead_data', {})
            email_data.append({
                'to': email['to'],
                'subject': email['subject'],
                'body': email['body'],
                'company_name': email['company_name'],
                'score': lead.get('score', 0),
                'industry': lead.get('industry', ''),
                'funding_stage': lead.get('funding_stage', ''),
                'website': lead.get('website', ''),
            })
        
        pd.DataFrame(email_data).to_csv(email_file, index=False)
        print(f"✓ Email campaign: {email_file}")
        
        # 4. Generate summary report
        report_file = f'summary_report_{timestamp}.txt'
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("LEAD GENERATION SUMMARY REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("OVERALL STATS\n")
            f.write("-"*60 + "\n")
            f.write(f"Total Leads Collected: {len(self.all_leads)}\n")
            f.write(f"High-Quality Leads: {len(high_quality_leads)}\n")
            f.write(f"Emails Generated: {len(emails)}\n")
            f.write(f"Average Score: {sum(l['score'] for l in self.all_leads) / len(self.all_leads):.1f}\n\n")
            
            f.write("TOP 10 LEADS\n")
            f.write("-"*60 + "\n")
            for i, lead in enumerate(high_quality_leads[:10], 1):
                f.write(f"\n{i}. {lead.get('company_name')} (Score: {lead.get('score')})\n")
                f.write(f"   Industry: {lead.get('industry', 'N/A')}\n")
                f.write(f"   Funding: {lead.get('funding_stage', 'N/A')} - {lead.get('funding_amount', 'N/A')}\n")
                f.write(f"   Location: {lead.get('location', 'N/A')}\n")
                f.write(f"   Website: {lead.get('website', 'N/A')}\n")
            
            f.write("\n" + "="*60 + "\n")
            f.write("FILES GENERATED\n")
            f.write("-"*60 + "\n")
            f.write(f"• {leads_file}\n")
            f.write(f"• {hq_file}\n")
            f.write(f"• {email_file}\n")
            f.write(f"• {report_file}\n")
        
        print(f"✓ Summary report: {report_file}")
        
        return {
            'leads_file': leads_file,
            'hq_file': hq_file,
            'email_file': email_file,
            'report_file': report_file
        }
    
    def run_complete_pipeline(self, use_apis=False, min_score=50):
        """
        Run the complete lead generation pipeline
        """
        print("\n" + "╔" + "="*58 + "╗")
        print("║" + " "*10 + "ELEVATEDPIXELS LEAD GENERATION PIPELINE" + " "*8 + "║")
        print("╚" + "="*58 + "╝")
        
        start_time = datetime.now()
        
        try:
            # Step 1: Collect
            self.step1_collect_leads(use_apis=use_apis)
            
            # Step 2: Enrich
            if use_apis:
                self.step2_enrich_leads()
            
            # Step 3: Score & Filter
            high_quality = self.step3_score_and_filter(min_score=min_score)
            
            # Step 4: Generate Outreach
            emails = self.step4_generate_outreach(high_quality)
            
            # Step 5: Export
            files = self.step5_export_results(high_quality, emails)
            
            # Final summary
            duration = (datetime.now() - start_time).total_seconds()
            
            print("\n" + "="*60)
            print("✅ PIPELINE COMPLETE")
            print("="*60)
            print(f"Duration: {duration:.1f} seconds")
            print(f"Total Leads: {len(self.all_leads)}")
            print(f"Qualified Leads: {len(high_quality)}")
            print(f"Ready for Outreach: {len(emails)}")
            print("\nNext Steps:")
            print("1. Review high-quality leads in:", files['hq_file'])
            print("2. Customize emails in:", files['email_file'])
            print("3. Import to your CRM/email tool")
            print("4. Start outreach campaign!")
            print("="*60)
            
            return {
                'success': True,
                'total_leads': len(self.all_leads),
                'qualified_leads': len(high_quality),
                'files': files,
                'duration': duration
            }
            
        except Exception as e:
            logging.error(f"Pipeline failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """
    Run the complete pipeline
    """
    pipeline = LeadGenerationPipeline()
    
    # Configuration
    USE_APIS = False  # Set to True to use real APIs (requires API keys in config.py)
    MIN_SCORE = 30    # Minimum lead quality score (0-100)
    
    print("\n⚙️  Configuration:")
    print(f"   Use APIs: {'Yes (requires API keys)' if USE_APIS else 'No (using sample data)'}")
    print(f"   Minimum Score: {MIN_SCORE}")
    print(f"   Processing...\n")
    
    # Run pipeline
    results = pipeline.run_complete_pipeline(
        use_apis=USE_APIS,
        min_score=MIN_SCORE
    )
    
    if results['success']:
        print("\n🎉 Success! Check the generated files above.")
    else:
        print(f"\n❌ Pipeline failed: {results.get('error')}")


if __name__ == "__main__":
    main()
