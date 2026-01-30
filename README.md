# 👻 GhostHunter: Lead Generation & Data Intelligence Tool

**GhostHunter** is a specialized web scraping tool designed to identify "hidden gem" businesses on Google Maps. It finds businesses that perform well (high ratings/reviews) but **do not have an official website**, making them perfect leads for web development or digital marketing services.

## 🚀 Features

* **Smart Scraping:** Uses `Playwright` (headless browser) to navigate Google Maps like a real user.
* **Website Detection:** Distinguishes between a *real* website and "social-only" placeholders (e.g., Instagram, Facebook, Linktree).
* **Performance Scoring:** Calculates a unique "Opportunity Score" based on review volume and average rating.
* **Data Export:** automatically saves results to a clean **CSV file** and JSON (logic included).
* **Stealth Mode:** Mimics human browsing behavior to reduce detection.

---

## 🛠️ Installation

### 1. Prerequisites

Ensure you have **Python 3.8+** installed.

### 2. Install Dependencies

Open your terminal (PowerShell or Command Prompt) and run:

```bash
pip install playwright pandas

```

### 3. Install the Browser Engine

Since Playwright requires a specific browser binary, run this command (use `python -m` to avoid PATH issues):

```bash
python -m playwright install chromium

```

---

## 💻 Usage

1. **Open the script** `ghost_hunter.py` in your text editor (VS Code, Notepad++, etc.).
2. **Scroll to the bottom** of the file to the `__main__` section.
3. **Edit your search criteria**:

```python
if __name__ == "__main__":
    # Change these values to whatever you want to search for
    category_input = "Plumbers"       # e.g., "Dentists", "Roofers", "Gyms"
    location_input = "Miami, FL"      # e.g., "Austin, TX", "London, UK"
    
    engine = GhostHunterEngine()
    asyncio.run(engine.run(category_input, location_input))

```

4. **Run the script**:

```bash
python ghost_hunter.py

```

---

## 📊 Output Explanation

When the script finishes, it will generate a CSV file named like `leads_Plumbers_Miami,_FL.csv`.

### Columns in CSV:

| Column | Description |
| --- | --- |
| **Name** | Business Name |
| **Rating** | Google Maps Star Rating (1.0 - 5.0) |
| **Review Count** | Total number of reviews |
| **Website Status** | `NONE` (No link), `SOCIAL_ONLY` (FB/Insta link), or `OFFICIAL` |
| **Performance Score** | A calculated score. Higher = Better Lead. |
| **Phone** | Contact number if available |

---

## ⚙️ Architecture

The tool operates in four modular stages:

1. **The Scout:** Navigates Google Maps and scrolls through listings.
2. **The Filter:** Checks if the URL provided is a real domain or just a social media profile.
3. **The Judge:** Applies math to determine if the business is "performing well" (e.g., High Rating + No Website = High Opportunity).
4. **The Reporter:** Formats the data and saves it to CSV.

---

## ⚠️ Troubleshooting

**Issue: "playwright is not recognized as an internal or external command"**

* **Fix:** Use `python -m playwright install chromium` instead of just `playwright install`.

**Issue: Script crashes or times out**

* **Fix:** Google Maps is heavy. If your internet is slow, increase the timeout in the `search_businesses` function:
```python
await page.wait_for_selector('div[role="feed"]', timeout=30000) # Increase to 30000 (30 sec)

```



---

## ⚖️ Legal Disclaimer

This tool is for **educational and research purposes only**.

* Scraping Google Maps data may violate their Terms of Service.
* Do not use this tool for aggressive, high-volume scraping without proxies.
* Respect the privacy of business owners.
