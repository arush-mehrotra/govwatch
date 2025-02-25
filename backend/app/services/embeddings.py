import logging
import json
from typing import Dict, List, Any
from pinecone.grpc import PineconeGRPC as Pinecone
from app.config import PINECONE_API_KEY, GEMINI_API_KEY
from google import genai
from google.genai import types

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Initialize Gemini client
genai_client = genai.Client(api_key=GEMINI_API_KEY)

# Constants
INDEX_NAME = "govwatch"
EMBEDDING_MODEL = "text-embedding-004"  # Gemini's embedding model
BATCH_SIZE = 20  # Smaller batch size for Gemini API

def initialize_pinecone():
    """
    Initialize Pinecone and connect to the index
    """
    try:
        # Connect to the index
        index = pc.Index(INDEX_NAME)
        return index
    
    except Exception as e:
        logger.error(f"Error initializing Pinecone: {str(e)}")
        raise

async def generate_gemini_embedding(text: str) -> List[float]:
    """
    Generate an embedding for the given text using Gemini's API
    
    Args:
        text: The text to generate an embedding for
        
    Returns:
        List[float]: The embedding vector
    """
    try:
        # Truncate text if it's too long (Gemini has token limits)
        max_chars = 25000  # Gemini's limit may be different, adjust as needed
        if len(text) > max_chars:
            logger.warning(f"Text too long ({len(text)} chars), truncating to {max_chars} chars")
            text = text[:max_chars]
        
        # Generate embedding using Gemini
        result = genai_client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text
        )
        
        # Make sure we're returning a list of floats
        embeddings = result.embeddings
        values = embeddings[0].values
            
        return values
    
    except Exception as e:
        logger.error(f"Error generating Gemini embedding: {str(e)}")
        raise

async def generate_embeddings(contract_data: List[Dict[str, Any]]):
    """
    Process contract data, generate embeddings using Gemini, and upsert to Pinecone
    
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
            "total_sections": 0,
            "batches_processed": 0
        }
        
        # Process each contract
        for contract in contract_data:
            contract_url = contract["url"]
            contract_date = contract["date"]
            sections = contract["sections"]
            
            logger.info(f"Processing contract: {contract_url}")
            
            # Organize sections by namespace for batch processing
            namespace_sections = {}
            
            # Process each section
            for section_name, section_text in sections.items():
                # Skip empty sections
                if not section_text.strip():
                    logger.warning(f"Empty section '{section_name}' in contract {contract_url}")
                    continue
                
                # Generate a unique ID for this section
                article_id = contract_url.split("/")[-2] if contract_url.split("/")[-1] == "" else contract_url.split("/")[-1]
                vector_id = f"{article_id}_{section_name.replace(' ', '_')}"
                
                # Add to namespace collection
                if section_name not in namespace_sections:
                    namespace_sections[section_name] = []
                
                namespace_sections[section_name].append({
                    "id": vector_id,
                    "text": section_text,
                    "metadata": {
                        "contract_url": contract_url,
                        "date": contract_date,
                        "section": section_name,
                        "text": section_text[:1000]  # Store a preview of the text
                    }
                })
                
                stats["total_sections"] += 1
            
            # Process each namespace in batches
            for namespace, sections_list in namespace_sections.items():
                # Process in batches
                for i in range(0, len(sections_list), BATCH_SIZE):
                    batch = sections_list[i:i+BATCH_SIZE]
                    
                    try:
                        # Prepare vectors for upsert
                        vectors_to_upsert = []
                        
                        # Generate embeddings for each section in the batch
                        for section in batch:
                            try:
                                # Generate embedding using Gemini
                                embedding = await generate_gemini_embedding(section["text"])
                                
                                # Add to upsert list
                                vectors_to_upsert.append({
                                    "id": section["id"],
                                    "values": embedding,
                                    "metadata": section["metadata"]
                                })
                                
                                stats["successful_embeddings"] += 1
                                
                            except Exception as e:
                                logger.error(f"Error generating embedding for section {section['id']}: {str(e)}")
                                stats["failed_embeddings"] += 1
                        
                        # Upsert vectors to Pinecone
                        if vectors_to_upsert:
                            index.upsert(
                                vectors=vectors_to_upsert,
                                namespace=namespace
                            )
                            logger.info(f"Upserted {len(vectors_to_upsert)} vectors to namespace '{namespace}'")
                        
                        stats["batches_processed"] += 1
                        
                    except Exception as e:
                        logger.error(f"Error processing batch for namespace {namespace}: {str(e)}")
                        stats["failed_embeddings"] += len(batch)
        
        logger.info(f"Completed embedding process. Stats: {json.dumps(stats)}")
        return stats
    
    except Exception as e:
        logger.error(f"Error in generate_embeddings: {str(e)}")
        raise
