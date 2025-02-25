import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

class ContractScraper:
    """
    A class to scrape DoD contract information from defense.gov
    """
    
    def __init__(self, url: Optional[str] = None):
        """
        Initialize the scraper with an optional URL
        
        Args:
            url: The URL of the contract page to scrape
        """
        self.url = url
        self.soup = None
        
    def set_url(self, url: str) -> None:
        """
        Set or update the URL to scrape
        
        Args:
            url: The URL of the contract page to scrape
        """
        self.url = url
        self.soup = None  # Reset the soup when URL changes
        
    def fetch_page(self) -> bool:
        """
        Fetch the webpage content and prepare it for parsing
        
        Returns:
            bool: True if the page was successfully fetched, False otherwise
        """
        if not self.url:
            print("No URL provided")
            return False
            
        try:
            response = requests.get(self.url)
            if response.status_code != 200:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
                return False
                
            self.soup = BeautifulSoup(response.text, 'html.parser')
            return True
        except Exception as e:
            print(f"Error fetching page: {str(e)}")
            return False
    
    def extract_contract_date(self) -> str:
        """
        Extract and format the contract date from the page title
        
        Returns:
            str: The contract date in YYYY-MM-DD format or "Unknown Date" if not found
        """
        if not self.soup:
            return "Unknown Date"
            
        maintitle = self.soup.find("h1", class_="maintitle")
        if not maintitle:
            return "Unknown Date"
        
        title_text = maintitle.get_text(strip=True)
        # Convert "Contracts For Feb. 24, 2025" to "2025-02-24"
        try:
            from datetime import datetime
            date_str = title_text.replace("Contracts For ", "")
            parsed_date = datetime.strptime(date_str, "%b. %d, %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"Error parsing date: {str(e)}")
            return "Unknown Date"
    
    def extract_sections(self) -> Dict[str, str]:
        """
        Extract all sections and their paragraphs from the contract page
        
        Returns:
            Dict[str, str]: Dictionary with section names as keys and concatenated text as values
        """
        sections = {}
        
        if not self.soup:
            return sections
            
        body_div = self.soup.find('div', class_='body')
        if not body_div:
            return sections
            
        current_section = None
        
        # Loop through all <p> tags in the body
        for p in body_div.find_all('p'):
            # Check if the <p> tag is a section header (centered text with a <strong> tag)
            if p.has_attr('style') and 'text-align: center' in p['style']:
                strong_tag = p.find('strong')
                if strong_tag:
                    current_section = strong_tag.get_text(strip=True)
                    sections[current_section] = ""
            else:
                # Add the paragraph text to the current section's content
                if current_section:
                    text = p.get_text(strip=True)
                    if text:  # Only add non-empty paragraphs
                        # If there's already text, add a space before appending
                        if sections[current_section]:
                            sections[current_section] += " "
                        sections[current_section] += text
        
        return sections
    
    def scrape(self, url: Optional[str] = None) -> Dict:
        """
        Scrape the contract page and return structured data
        
        Args:
            url: Optional URL to scrape (will use the instance URL if not provided)
            
        Returns:
            Dict: Dictionary containing the contract date and sections with their content
        """
        if url:
            self.set_url(url)
            
        if not self.fetch_page():
            return {"error": "Failed to fetch page"}
            
        contract_date = self.extract_contract_date()
        sections = self.extract_sections()
        
        return {
            "date": contract_date,
            "sections": sections
        }


# Example usage:
if __name__ == "__main__":
    scraper = ContractScraper()
    result = scraper.scrape("https://www.defense.gov/News/Contracts/Contract/Article/4076032/")
    
    print(f"Contract Date: {result['date']}")
    print("\nExtracted Sections:")
    for section, text in result['sections'].items():
        print(f"\nSection: {section}")
        print(f"Text: {text[:200]}...")  # Print first 200 chars of each section
