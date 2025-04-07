import logging
import json
from typing import Dict, List, Any, AsyncGenerator
from pinecone.grpc import PineconeGRPC as Pinecone
from app.config import PINECONE_API_KEY, GEMINI_API_KEY
from google import genai
from google.genai import types
from fastapi.responses import StreamingResponse

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Pinecone
logger.info(f"Pinecone client version: {Pinecone.__module__}")
pc = Pinecone(api_key=PINECONE_API_KEY)

# Try with environment parameter if needed
# pc = Pinecone(api_key=PINECONE_API_KEY, environment="gcp-starter")

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
        # Debug logging
        logger.info(f"Initializing Pinecone with API key: {PINECONE_API_KEY[:5]}... (first 5 chars only)")
        logger.info(f"Using index name: {INDEX_NAME}")
        
        # List available indexes
        try:
            indexes = pc.list_indexes()
            logger.info(f"Available Pinecone indexes: {indexes}")
            
            if INDEX_NAME not in [idx.name for idx in indexes]:
                logger.warning(f"Index '{INDEX_NAME}' not found in available indexes!")
        except Exception as list_err:
            logger.warning(f"Could not list indexes: {str(list_err)}")
        
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
    All vectors will be stored in a single namespace
    
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
        
        # Collect all sections across all contracts
        all_sections = []
        
        # Process each contract
        for contract in contract_data:
            contract_url = contract["url"]
            contract_date = contract["date"]
            sections = contract["sections"]
            
            logger.info(f"Processing contract: {contract_url}")
            
            # Process each section
            for section_name, section_text in sections.items():
                # Skip empty sections
                if not section_text.strip():
                    logger.warning(f"Empty section '{section_name}' in contract {contract_url}")
                    continue
                
                # Generate a unique ID for this section
                article_id = contract_url.split("/")[-2] if contract_url.split("/")[-1] == "" else contract_url.split("/")[-1]
                vector_id = f"{article_id}_{section_name.replace(' ', '_')}"
                
                # Add to collection
                all_sections.append({
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
        
        # Process all sections in batches
        for i in range(0, len(all_sections), BATCH_SIZE):
            batch = all_sections[i:i+BATCH_SIZE]
            
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
                
                # Upsert vectors to Pinecone (using a single namespace)
                if vectors_to_upsert:
                    # Use a single namespace for all vectors
                    # You can use an empty string or a specific namespace name
                    index.upsert(
                        vectors=vectors_to_upsert,
                        namespace="contracts"  # Single namespace for all contracts
                    )
                    logger.info(f"Upserted {len(vectors_to_upsert)} vectors to namespace 'contracts'")
                
                stats["batches_processed"] += 1
                
            except Exception as e:
                logger.error(f"Error processing batch {i//BATCH_SIZE + 1}: {str(e)}")
                stats["failed_embeddings"] += len(batch)
        
        logger.info(f"Completed embedding process. Stats: {json.dumps(stats)}")
        return stats
    
    except Exception as e:
        logger.error(f"Error in generate_embeddings: {str(e)}")
        raise

async def search_with_gemini(query: str, top_k: int = 5):
    """
    Search for contracts using a natural language query and generate a response using Gemini
    
    Args:
        query: The natural language search query
        top_k: Number of results to retrieve from Pinecone
        
    Returns:
        Dict: Response containing the answer and sources
    """
    try:
        # Initialize Pinecone
        index = initialize_pinecone()
        
        # Generate embedding for the query using Gemini
        query_embedding = await generate_gemini_embedding(query)
        
        # Search in Pinecone
        search_response = index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace="contracts",  # Using the single namespace we defined
            include_metadata=True
        )
        
        # Extract relevant context from search results
        contexts = []
        sources = []
        
        for match in search_response.matches:
            # Add the text as context
            context_text = match.metadata.get("text", "")
            if context_text:
                contexts.append(context_text)
            
            # Add source information
            sources.append({
                "score": match.score,
                "contract_url": match.metadata.get("contract_url", ""),
                "date": match.metadata.get("date", ""),
                "section": match.metadata.get("section", "")
            })
        
        # If no contexts found, return early
        if not contexts:
            return {
                "answer": "I couldn't find any relevant information about your query in the contracts database.",
                "sources": []
            }
        
        # Combine contexts into a single string
        combined_context = "\n\n".join(contexts)
        
        # Prepare prompt for Gemini
        prompt = f"""
        You are an AI assistant specialized in analyzing Department of Defense contracts.
        
        USER QUERY: {query}
        
        RELEVANT CONTRACT INFORMATION:
        {combined_context}
        
        Based ONLY on the information provided above, please answer the user's query.
        Format your response using proper markdown:
        - Use complete pairs of double asterisks for bold text (e.g., **Company Name**)
        - Ensure all asterisks are properly closed
        - Use proper numbered lists (1., 2., etc.)
        - Format dollar amounts consistently
        
        If the information doesn't contain an answer to the query, say so clearly.
        Include specific details from the contracts when relevant.
        """
        
        # Generate response using Gemini
        generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        # Return the answer and sources
        return {
            "answer": response.text,
            "sources": sources
        }
    
    except Exception as e:
        logger.error(f"Error in search_with_gemini: {str(e)}")
        raise

async def search_with_gemini_stream(query: str, top_k: int = 5) -> AsyncGenerator[str, None]:
    """
    Search for contracts using a natural language query and generate a streaming response using Gemini
    
    Args:
        query: The natural language search query
        top_k: Number of results to retrieve from Pinecone
        
    Returns:
        AsyncGenerator: Streaming response from Gemini
    """
    try:
        # Initialize Pinecone
        index = initialize_pinecone()
        
        # Generate embedding for the query using Gemini
        query_embedding = await generate_gemini_embedding(query)
        
        # Search in Pinecone
        search_response = index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace="contracts",  # Using the single namespace we defined
            include_metadata=True
        )
        
        # Extract relevant context from search results
        contexts = []
        sources = []
        
        for match in search_response.matches:
            # Add the text as context
            context_text = match.metadata.get("text", "")
            if context_text:
                contexts.append(context_text)
            
            # Add source information
            sources.append({
                "score": match.score,
                "contract_url": match.metadata.get("contract_url", ""),
                "date": match.metadata.get("date", ""),
                "section": match.metadata.get("section", "")
            })
        
        # If no contexts found, yield a message and return
        if not contexts:
            yield "I couldn't find any relevant information about your query in the contracts database."
            return
        
        # Combine contexts into a single string
        combined_context = "\n\n".join(contexts)
        
        # Prepare prompt for Gemini
        prompt = f"""
        You are an AI assistant specialized in analyzing Department of Defense contracts.
        
        USER QUERY: {query}
        
        RELEVANT CONTRACT INFORMATION:
        {combined_context}
        
        Based ONLY on the information provided above, please answer the user's query.
        Format your response using proper markdown:
        - Use complete pairs of double asterisks for bold text (e.g., **Company Name**)
        - Ensure all asterisks are properly closed
        - Use proper numbered lists (1., 2., etc.)
        - Format dollar amounts consistently
        
        If the information doesn't contain an answer to the query, say so clearly.
        Include specific details from the contracts when relevant.
        """
        
        # Generate streaming response using Gemini
        generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        # Use the streaming version of generate_content
        response_stream = genai_client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Stream the response chunks
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    
    except Exception as e:
        error_msg = f"Error in search_with_gemini_stream: {str(e)}"
        logger.error(error_msg)
        yield f"Error: {error_msg}"
