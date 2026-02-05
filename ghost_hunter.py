import asyncio
import random
import re
import pandas as pd
import json
import logging
from dataclasses import dataclass, asdict
from typing import List, Optional
from playwright.async_api import async_playwright, Page

# --- CONFIGURATION & CONSTANTS ---
SOCIAL_DOMAINS = [
    "facebook.com", "instagram.com", "yelp.com", 
    "linkedin.com", "whatsapp.com", "twitter.com", 
    "tiktok.com", "linktr.ee"
]

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# --- DATA MODELS ---
@dataclass
class BusinessEntity:
    name: str
    category: str
    location: str
    rating: float
    review_count: int
    url: Optional[str]
    phone: Optional[str]
    website_status: str  # 'OFFICIAL', 'SOCIAL_ONLY', 'NONE'
    performance_score: float

# --- LOGIC MODULES ---

class WebsiteValidator:
    """Analyzes a URL to determine if it is a real website or a social placeholder."""
    
    @staticmethod
    def classify_url(url: str) -> str:
        if not url:
            return "NONE"
        
        # Normalize
        url_lower = url.lower()
        
        # Check if it points to a social media platform
        for domain in SOCIAL_DOMAINS:
            if domain in url_lower:
                return "SOCIAL_ONLY"
        
        return "OFFICIAL"

class PerformanceScorer:
    """Calculates a business potential score."""
    
    @staticmethod
    def calculate_score(rating: float, reviews: int) -> float:
        # Algorithm:
        # Base score on rating (0-50 points)
        # Multiplier based on review volume (logarithmic scale)
        # We want high ratings + high volume to win.
        
        if reviews == 0:
            return 0.0
            
        rating_score = (rating / 5.0) * 50  # Max 50
        
        # Volume bonus: Cap at 50 points for 500+ reviews
        import math
        volume_score = min(50, math.log(reviews) * 8) 
        
        total = rating_score + volume_score
        return round(total, 2)

class MapsScraper:
    """Handles the browser interaction with Google Maps."""
    
    def __init__(self, headless=True):
        self.headless = headless

    async def search_businesses(self, query: str, limit: int = 20) -> List[dict]:
        async with async_playwright() as p:
            # Launch browser with stealth-like args
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            
            logger.info(f"Navigating to Google Maps for query: {query}")
            await page.goto(f"https://www.google.com/maps/search/{query}")
            await page.wait_for_selector('div[role="feed"]', timeout=15000)

            # Scroll loop to load results
            results = []
            seen_urls = set()
            
            logger.info("Scraping results...")
            
            while len(results) < limit:
                # Select all business cards
                cards = await page.locator('div[role="article"]').all()
                
                # If no cards found, break
                if not cards:
                    break

                for card in cards:
                    if len(results) >= limit: 
                        break

                    try:
                        # Extract basic info via Aria Labels or Text
                        # Note: Selectors in Maps are obfuscated. We use robust locators where possible.
                        aria_label = await card.get_attribute("aria-label")
                        if not aria_label or aria_label in seen_urls:
                            continue
                        
                        name = aria_label
                        seen_urls.add(name)

                        # Click the card to load details in the side panel (necessary for URL/Phone)
                        await card.click()
                        await page.wait_for_timeout(1000) # Respectful pause
                        
                        # Extract Details from the main pane
                        data = await self._extract_details(page, name)
                        if data:
                            results.append(data)
                            logger.info(f"Found: {data['name']} | Rating: {data['rating']}")

                    except Exception as e:
                        # Skip errors on individual cards to keep pipeline moving
                        continue
                
                # Scroll down the feed
                await page.locator('div[role="feed"]').evaluate("node => node.scrollTop += 5000")
                await page.wait_for_timeout(2000)
                
                # Check for "You've reached the end" logic (omitted for brevity)

            await browser.close()
            return results

    async def _extract_details(self, page: Page, name: str) -> Optional[dict]:
        """Extracts detailed info from the currently open business panel."""
        try:
            # Helper to get text safe
            text_content = await page.content()
            
            # Extract Rating & Reviews using Aria label strategy or specific classes
            # Example aria-label: "4.5 stars 120 Reviews"
            rating = 0.0
            reviews = 0
            
            # Try finding the rating star icon container
            rating_el = page.locator('span[role="img"][aria-label*="stars"]')
            if await rating_el.count() > 0:
                rating_str = await rating_el.first.get_attribute("aria-label")
                # Parse "4.5 stars 120 Reviews"
                match = re.search(r"([\d\.]+)\s+stars\s+([\d,]+)\s+Reviews", rating_str, re.IGNORECASE)
                if match:
                    rating = float(match.group(1))
                    reviews = int(match.group(2).replace(",", ""))

            # Extract Website
            # The website button usually has data-value="URL" or specific icon
            website_url = None
            website_btn = page.locator('a[data-item-id="authority"]')
            if await website_btn.count() > 0:
                website_url = await website_btn.get_attribute("href")

            # Extract Phone
            phone = None
            phone_btn = page.locator('button[data-item-id*="phone:tel:"]')
            if await phone_btn.count() > 0:
                phone = await phone_btn.get_attribute("aria-label")
                if phone: phone = phone.replace("Phone: ", "")

            return {
                "name": name,
                "rating": rating,
                "review_count": reviews,
                "url": website_url,
                "phone": phone
            }

        except Exception as e:
            logger.error(f"Error extracting details: {e}")
            return None

# --- ORCHESTRATOR ---

class GhostHunterEngine:
    def __init__(self):
        self.scraper = MapsScraper(headless=False) # Headless=False to see it working
    
    async def run(self, category: str, location: str):
        query = f"{category} in {location}"
        logger.info(f"Starting GhostHunter for: {query}")
        
        # 1. Scrape
        raw_data = await self.scraper.search_businesses(query, limit=15)
        
        # 2. Process & Filter
        processed_leads = []
        
        for item in raw_data:
            # Determine Website Status
            status = WebsiteValidator.classify_url(item['url'])
            
            # Calculate Score
            score = PerformanceScorer.calculate_score(item['rating'], item['review_count'])
            
            entity = BusinessEntity(
                name=item['name'],
                category=category,
                location=location,
                rating=item['rating'],
                review_count=item['review_count'],
                url=item['url'],
                phone=item['phone'],
                website_status=status,
                performance_score=score
            )
            
            # 3. Filtering Logic (The "Gold" Criteria)
            # We want businesses with NO official website but GOOD performance.
            is_opportunity = (
                (entity.website_status in ["NONE", "SOCIAL_ONLY"]) and
                (entity.rating >= 4.0) and
                (entity.review_count >= 15) # Lowered threshold for demo
            )
            
            if is_opportunity:
                processed_leads.append(asdict(entity))

        # 4. Output
        if processed_leads:
            df = pd.DataFrame(processed_leads)
            df = df.sort_values(by="performance_score", ascending=False)
            
            # Export
            filename = f"leads_{category}_{location}.csv".replace(" ", "_")
            df.to_csv(filename, index=False)
            logger.info(f"Successfully exported {len(df)} leads to {filename}")
            
            # Print Preview
            print("\n--- TOP LEADS FOUND ---")
            print(df[['name', 'rating', 'review_count', 'website_status', 'performance_score']].head())
        else:
            logger.info("No leads found matching criteria.")

# --- ENTRY POINT ---
if __name__ == "__main__":
    # Example Usage
    category_input = "Italian Restaurants"
    location_input = "Vadodara, IN"
    
    engine = GhostHunterEngine()
    asyncio.run(engine.run(category_input, location_input))