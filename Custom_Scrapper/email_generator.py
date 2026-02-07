"""
Email Outreach Template Generator
Generates personalized outreach emails for qualified leads
"""

from typing import Dict
import random


class EmailOutreachGenerator:
    """
    Generates personalized email templates for different lead types
    """
    
    def __init__(self):
        self.sender_name = "Jeet & Prince"
        self.company_name = "ElevatedPixels"
        self.website = "https://elevatedpixels.app"
    
    def generate_email(self, lead: Dict, template_type: str = 'funded_startup') -> Dict:
        """
        Generate personalized email based on lead type
        
        template_types:
        - funded_startup: Recently funded companies
        - outdated_website: Companies with poor website performance
        - cold_outreach: General outreach
        - referral: From referral or mutual connection
        """
        
        templates = {
            'funded_startup': self._funded_startup_template,
            'outdated_website': self._outdated_website_template,
            'cold_outreach': self._cold_outreach_template,
            'referral': self._referral_template,
        }
        
        generator = templates.get(template_type, self._cold_outreach_template)
        return generator(lead)
    
    def _funded_startup_template(self, lead: Dict) -> Dict:
        """Template for recently funded startups"""
        
        company_name = lead.get('company_name', '[Company]')
        funding_stage = lead.get('funding_stage', 'recent funding')
        funding_amount = lead.get('funding_amount', '')
        industry = lead.get('industry', 'tech')
        
        subject_lines = [
            f"Congrats on the {funding_stage} round, {company_name}",
            f"Helping {funding_stage} companies scale their digital presence",
            f"{company_name}'s growth + ElevatedPixels = 🚀",
        ]
        
        body = f"""Hi there,

Congrats on your {funding_stage} round{f' of {funding_amount}' if funding_amount else ''}! I came across {company_name} and was impressed by what you're building in the {industry} space.

As you scale post-funding, your digital presence becomes crucial. We're ElevatedPixels, and we specialize in building high-performance web experiences for funded startups like yours.

Here's what we bring to the table:
• Strategic web design that converts visitors into users
• Lightning-fast, scalable architecture (React, Vue, modern stacks)
• Zero technical debt – built for growth from day one

We've helped companies at your stage:
✓ Reduce page load times by 50%+
✓ Improve conversion rates with data-driven UX
✓ Build platforms that scale with their growth

Would you be open to a quick 15-minute call to explore how we can support {company_name}'s next chapter?

Best,
{self.sender_name}
{self.company_name}
{self.website}

P.S. We're currently working with [similar company] and [similar company]. Happy to share case studies if interested.
"""
        
        return {
            'subject': random.choice(subject_lines),
            'body': body,
            'to': lead.get('contact_email', ''),
            'company_name': company_name
        }
    
    def _outdated_website_template(self, lead: Dict) -> Dict:
        """Template for companies with website issues"""
        
        company_name = lead.get('company_name', '[Company]')
        website = lead.get('website', '')
        load_time = lead.get('load_time', 0)
        
        subject_lines = [
            f"Quick observation about {company_name}'s website",
            f"Your website could be costing you customers",
            f"Performance opportunity for {company_name}",
        ]
        
        issues_found = []
        if load_time > 3:
            issues_found.append(f"• Load time of {load_time}s (industry standard is <2s)")
        
        analysis = lead.get('website_analysis', {})
        if analysis.get('has_mobile_issues'):
            issues_found.append("• Mobile responsiveness issues detected")
        if analysis.get('is_outdated'):
            issues_found.append("• Using outdated web technologies")
        
        issues_text = '\n'.join(issues_found) if issues_found else "• Some optimization opportunities"
        
        body = f"""Hi,

I was checking out {company_name} and noticed a few things about your website that might be impacting conversions:

{issues_text}

These issues could be costing you customers – especially on mobile, where 60% of users will leave if a page takes >3 seconds to load.

We're ElevatedPixels, and we specialize in building modern, high-performance websites that actually convert. Our approach:

1. Strategy-first design (not just "pretty")
2. Modern tech stack (React/Vue for speed)
3. Built for conversions, not just aesthetics

We've helped similar companies:
• Reduce bounce rates by 40%
• Improve load times by 50%+
• Increase mobile conversions by 2x

Would you be interested in a free website audit? I can share specific recommendations for {company_name} – no strings attached.

Best,
{self.sender_name}
{self.company_name}
{self.website}

P.S. I can send over the full audit report by end of week if you're interested.
"""
        
        return {
            'subject': random.choice(subject_lines),
            'body': body,
            'to': lead.get('contact_email', ''),
            'company_name': company_name
        }
    
    def _cold_outreach_template(self, lead: Dict) -> Dict:
        """General cold outreach template"""
        
        company_name = lead.get('company_name', '[Company]')
        industry = lead.get('industry', 'industry')
        
        subject_lines = [
            f"Quick question about {company_name}'s digital strategy",
            f"Building better web experiences for {industry} companies",
            f"{company_name} + ElevatedPixels?",
        ]
        
        body = f"""Hi,

I've been following {company_name} and love what you're doing in {industry}.

I'm reaching out because we work with companies like yours to build web experiences that actually drive business results. We're ElevatedPixels – a web development studio that bridges the gap between great design and solid engineering.

What sets us apart:
• We don't just build websites; we engineer digital ecosystems
• Modern tech stack (React, Vue, WebGL) for speed and scalability
• Strategy-first approach – form follows function

Quick question: Are you currently happy with your website's performance and conversion rates?

If not, I'd love to share how we've helped similar companies in {industry}:
✓ 50%+ faster load times
✓ 2x improvement in user retention
✓ 100% scalable architecture

Would a quick 15-minute call make sense to explore potential synergies?

Best,
{self.sender_name}
{self.company_name}
{self.website}

P.S. No sales pitch – just genuinely curious about your current challenges and happy to offer insights.
"""
        
        return {
            'subject': random.choice(subject_lines),
            'body': body,
            'to': lead.get('contact_email', ''),
            'company_name': company_name
        }
    
    def _referral_template(self, lead: Dict) -> Dict:
        """Template for referral-based outreach"""
        
        company_name = lead.get('company_name', '[Company]')
        referrer = lead.get('referrer_name', '[Mutual Connection]')
        
        subject_lines = [
            f"{referrer} recommended I reach out",
            f"Introduction from {referrer}",
            f"{referrer} thought we should connect",
        ]
        
        body = f"""Hi,

{referrer} mentioned that {company_name} might be looking to upgrade your digital presence, so I wanted to reach out.

We're ElevatedPixels – we specialize in building high-performance web experiences for growing companies. {referrer} has seen our work with [previous client] and thought we'd be a great fit for {company_name}.

Our approach is different:
• Strategy before pixels – we start with your business goals
• Modern, scalable tech stack (React/Vue)
• Designed for performance and conversions

We've helped companies like [similar company] and [similar company]:
✓ Reduce page load times by 50%
✓ Improve conversion rates with data-driven UX
✓ Build platforms that scale with growth

Would you be open to a quick intro call? I can share specific case studies relevant to {company_name}.

Best,
{self.sender_name}
{self.company_name}
{self.website}

P.S. {referrer} mentioned you're [specific challenge]. Happy to share how we've tackled similar challenges.
"""
        
        return {
            'subject': random.choice(subject_lines),
            'body': body,
            'to': lead.get('contact_email', ''),
            'company_name': company_name
        }
    
    def generate_follow_up(self, lead: Dict, days_since_first: int) -> Dict:
        """Generate follow-up email"""
        
        company_name = lead.get('company_name', '[Company]')
        
        if days_since_first <= 3:
            subject = f"Re: {company_name} + ElevatedPixels"
            body = f"""Hi,

Just following up on my email from a few days ago. I know inboxes get busy!

Still curious if you'd be interested in exploring how we could help elevate {company_name}'s web presence.

If now's not the right time, no worries – feel free to reach out when it makes sense.

Best,
{self.sender_name}
"""
        elif days_since_first <= 7:
            subject = f"One last note about {company_name}"
            body = f"""Hi,

I wanted to reach out one more time before I close the loop.

If improving your website's performance and conversions isn't a priority right now, totally understand.

But if you'd like to chat about it sometime, my calendar is always open: [calendar link]

Either way, best of luck with {company_name}!

Best,
{self.sender_name}
"""
        else:
            subject = f"New resource for {company_name}"
            body = f"""Hi,

Hope all is well! I wanted to share a quick resource we just published: [relevant blog post/case study]

Thought it might be useful for {company_name} given what you're working on.

No ask – just sharing something that might be helpful!

Best,
{self.sender_name}
"""
        
        return {
            'subject': subject,
            'body': body,
            'to': lead.get('contact_email', ''),
            'company_name': company_name
        }
    
    def export_email_campaign(self, leads: list, output_file: str = 'email_campaign.csv'):
        """Export emails to CSV for mail merge"""
        import pandas as pd
        
        emails = []
        for lead in leads:
            # Determine best template based on lead data
            if lead.get('funding_stage') and lead.get('funding_date'):
                template_type = 'funded_startup'
            elif lead.get('website_analysis', {}).get('needs_redesign'):
                template_type = 'outdated_website'
            else:
                template_type = 'cold_outreach'
            
            email = self.generate_email(lead, template_type)
            email['lead_score'] = lead.get('score', 0)
            email['industry'] = lead.get('industry', '')
            email['funding_stage'] = lead.get('funding_stage', '')
            emails.append(email)
        
        df = pd.DataFrame(emails)
        df.to_csv(output_file, index=False)
        print(f"✅ Email campaign exported to {output_file}")
        
        return output_file


def main():
    """
    Example usage
    """
    generator = EmailOutreachGenerator()
    
    # Example lead
    lead = {
        'company_name': 'TechFlow AI',
        'funding_stage': 'Series A',
        'funding_amount': '$8M',
        'industry': 'SaaS',
        'contact_email': 'founders@techflow.ai',
        'website': 'https://techflow.ai',
        'load_time': 4.5,
        'website_analysis': {
            'needs_redesign': True,
            'has_mobile_issues': True
        }
    }
    
    # Generate different email types
    print("=" * 60)
    print("FUNDED STARTUP EMAIL")
    print("=" * 60)
    email1 = generator.generate_email(lead, 'funded_startup')
    print(f"Subject: {email1['subject']}")
    print(f"\n{email1['body']}\n")
    
    print("=" * 60)
    print("OUTDATED WEBSITE EMAIL")
    print("=" * 60)
    email2 = generator.generate_email(lead, 'outdated_website')
    print(f"Subject: {email2['subject']}")
    print(f"\n{email2['body']}\n")
    
    print("=" * 60)
    print("FOLLOW-UP EMAIL (Day 3)")
    print("=" * 60)
    email3 = generator.generate_follow_up(lead, 3)
    print(f"Subject: {email3['subject']}")
    print(f"\n{email3['body']}\n")


if __name__ == "__main__":
    main()
