from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from datetime import datetime, timedelta
import requests
import re
from bs4 import BeautifulSoup
import logging
from app.services.scraper import ContractScraper
from app.services.embeddings import generate_embeddings, search_with_gemini

# Optional: Import your vector embedding service
# from app.services.embeddings import generate_embeddings

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"]
)

logger = logging.getLogger(__name__)

async def process_contract_embeddings():
    """
    Process contracts and generate embeddings
    """
    try:
        # Get date range (yesterday to 7 days ago)
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=6)
        
        # Format dates for URL
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        # Construct URL
        url = f"https://www.defense.gov/News/Contracts/StartDate/{start_date_str}/EndDate/{end_date_str}/"

        print(url)
        
        logger.info(f"Processing contracts from {url} for embeddings")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Fetch the contracts listing page
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(f"Failed to retrieve contracts listing. Status code: {response.status_code}")
            return {"status": "error", "message": f"Failed to retrieve contracts listing. Status code: {response.status_code}"}
        
        # Parse the page to find contract links
        soup = BeautifulSoup(response.text, 'html.parser')
        contract_links = []

        for elem in soup.find_all("listing-titles-only"):
            # Try to get the absolute URL attribute first
            url = elem.get("article-url-or-link-absolute")
            # Fallback to relative URL if needed
            if not url:
                url = elem.get("article-url-or-link")
                if url and not url.startswith("http"):
                    url = f"https://www.defense.gov{url}"
            
            # Extract the publish date for constructing the title if needed
            publish_date = elem.get("publish-date-ap", "").strip()
            # Sometimes article-title may be empty for contracts, so we build a title
            title = elem.get("article-title", "").strip()
            if not title and publish_date:
                title = f"Contracts For {publish_date}"
            
            if url:
                print(f"Found contract: {title} at {url}")
                contract_links.append(url)


        logger.info(f"Processing {len(contract_links)} contracts for embeddings")

        # Debug output if no contracts found
        if not contract_links:
            logger.error("No contracts found. HTML structure:")
            html_sample = soup.prettify()  # Print the whole HTML (or part of it)
            with open("debug_html_sample.html", "w", encoding="utf-8") as f:
                f.write(html_sample)
            print("HTML structure saved to debug_html_sample.html")

            # Look for any links that might be contract related
            all_links = soup.find_all("a")
            contract_related = [link for link in all_links if "contract" in link.get("href", "").lower()]
            print(f"Found {len(contract_related)} potentially contract-related links:")
            for link in contract_related[:5]:
                print(f"  - {link.get('href')}: {link.get_text(strip=True)}")
        
        # Initialize scraper
        scraper = ContractScraper()
        
        # Process each contract
        contract_data = []
        processed_count = 0
        error_count = 0
        
        for url in contract_links:
            try:
                # Scrape the contract
                contract_info = scraper.scrape(url)
                
                # Add to our collection
                contract_data.append({
                    "url": url,
                    "date": contract_info["date"],
                    "sections": contract_info["sections"]
                })
                
                logger.info(f"Successfully processed contract: {url}")
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing contract {url}: {str(e)}")
                error_count += 1
        
        # Generate and store embeddings
        if contract_data:
            try:
                embedding_stats = await generate_embeddings(contract_data)
                logger.info(f"Embedding stats: {embedding_stats}")
            except Exception as e:
                logger.error(f"Error generating embeddings: {str(e)}")
                error_count += 1
        
        logger.info(f"Completed processing {len(contract_data)} contracts for embeddings")
        
        return {
            "status": "success",
            "date_range": {
                "start_date": start_date_str,
                "end_date": end_date_str
            },
            "stats": {
                "total_links_found": len(contract_links),
                "successfully_processed": processed_count,
                "errors": error_count
            }
        }
        
    except Exception as e:
        error_msg = f"Error in contract embedding process: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg}

@router.get("/test/process-embeddings")
async def test_process_embeddings():
    """
    Test endpoint for the process_contract_embeddings function
    Remove this in production
    """
    result = await process_contract_embeddings()
    return result

@router.post("/search")
async def search_contracts(query: str):
    """
    Search for contracts using a natural language query
    
    Args:
        query: The search query
        
    Returns:
        Dict: Response containing the answer and sources
    """
    try:
        if not query or len(query.strip()) < 3:
            raise HTTPException(status_code=400, detail="Query must be at least 3 characters long")
        
        result = await search_with_gemini(query)
        return result
    
    except Exception as e:
        logger.error(f"Error searching contracts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
