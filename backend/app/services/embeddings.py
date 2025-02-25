import logging
import json
from typing import Dict, List, Any
from pinecone import Pinecone, ServerlessSpec
from app.config import PINECONE_API_KEY

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Constants
INDEX_NAME = "govwatch"
EMBEDDING_DIMENSION = 1536  # Dimension for text-embedding-3-small

def initialize_pinecone():
    """
    Initialize Pinecone and create the index if it doesn't exist
    """
    try:
        # Check if our index already exists
        if INDEX_NAME not in [index.name for index in pc.list_indexes()]:
            logger.info(f"Creating new Pinecone index: {INDEX_NAME}")
            
            # Create a new index with OpenAI embedding model
            pc.create_index(
                name=INDEX_NAME,
                dimension=EMBEDDING_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-west-2")
            )
            logger.info(f"Successfully created index: {INDEX_NAME}")
        else:
            logger.info(f"Index {INDEX_NAME} already exists")
            
        # Connect to the index
        index = pc.Index(INDEX_NAME)
        return index
    
    except Exception as e:
        logger.error(f"Error initializing Pinecone: {str(e)}")
        raise

def process_contract_embeddings(contract_data: List[Dict[str, Any]]):
    """
    Process contract data and upsert to Pinecone with direct embedding
    
    Args:
        contract_data: List of contract dictionaries with date, sections, and URL
    
    Returns:
        Dict: Statistics about the processing
    """
    try:
        # Initialize Pinecone
        index = initialize_pinecone()
        
        stats = {
            "total_contracts": len(contract_data),
            "successful_embeddings": 0,
            "failed_embeddings": 0,
            "total_sections": 0
        }
        
        # Process each contract
        for contract in contract_data:
            contract_url = contract["url"]
            contract_date = contract["date"]
            sections = contract["sections"]
            
            logger.info(f"Processing contract: {contract_url}")
            
            # Process each section as a separate vector with its own namespace
            for section_name, section_text in sections.items():
                try:
                    # Skip empty sections
                    if not section_text.strip():
                        logger.warning(f"Empty section '{section_name}' in contract {contract_url}")
                        continue
                    
                    # Generate a unique ID for this section
                    # Extract article ID from URL for more stable IDs
                    article_id = contract_url.split("/")[-2] if contract_url.split("/")[-1] == "" else contract_url.split("/")[-1]
                    vector_id = f"{article_id}_{section_name.replace(' ', '_')}"
                    
                    # Truncate text if it's too long (Pinecone has limits)
                    max_chars = 32000
                    if len(section_text) > max_chars:
                        logger.warning(f"Text too long ({len(section_text)} chars), truncating to {max_chars} chars")
                        section_text = section_text[:max_chars]
                    
                    # Prepare metadata
                    metadata = {
                        "contract_url": contract_url,
                        "date": contract_date,
                        "section": section_name,
                        "text": section_text[:1000]  # Store a preview of the text
                    }
                    
                    # Upsert to Pinecone with section name as namespace
                    # Let Pinecone handle the embedding generation
                    index.upsert(
                        vectors=[
                            {
                                "id": vector_id,
                                "values": section_text,  # Pinecone will generate embedding from this text
                                "metadata": metadata
                            }
                        ],
                        namespace=section_name
                    )
                    
                    logger.info(f"Successfully embedded section '{section_name}' from {contract_url}")
                    stats["successful_embeddings"] += 1
                    stats["total_sections"] += 1
                    
                except Exception as e:
                    logger.error(f"Error processing section '{section_name}' from {contract_url}: {str(e)}")
                    stats["failed_embeddings"] += 1
        
        logger.info(f"Completed embedding process. Stats: {json.dumps(stats)}")
        return stats
    
    except Exception as e:
        logger.error(f"Error in process_contract_embeddings: {str(e)}")
        raise

def search_contracts(query: str, top_k: int = 5, namespace: str = None):
    """
    Search for contracts using a query string
    
    Args:
        query: The search query
        top_k: Number of results to return
        namespace: Optional namespace to search in (e.g., "ARMY", "NAVY")
        
    Returns:
        List: Matching contract sections
    """
    try:
        # Initialize Pinecone
        index = initialize_pinecone()
        
        # Search in Pinecone (Pinecone will generate the embedding for the query)
        search_response = index.query(
            vector=query,  # Pinecone will generate embedding from this text
            top_k=top_k,
            namespace=namespace,
            include_metadata=True
        )
        
        # Format results
        results = []
        for match in search_response.matches:
            results.append({
                "score": match.score,
                "contract_url": match.metadata["contract_url"],
                "date": match.metadata["date"],
                "section": match.metadata["section"],
                "text_preview": match.metadata["text"]
            })
        
        return results
    
    except Exception as e:
        logger.error(f"Error searching contracts: {str(e)}")
        raise
