# GovWatch Backend

The GovWatch backend is a FastAPI application that scrapes, processes, and provides search capabilities for government contracts using vector embeddings and AI.

## Architecture Overview

The backend consists of three main components:

1. **Contract Scraper**: Scrapes defense.gov for contract information
2. **Embeddings Service**: Generates vector embeddings using Gemini API and stores them in Pinecone
3. **Search API**: Provides semantic search capabilities for contracts using vector embeddings

## Prerequisites

- Python 3.11+
- Poetry (dependency management)
- Pinecone account (for vector database)
- Google Gemini API key

## Environment Setup

1. Clone the repository
2. Navigate to the backend directory
3. Create a `.env` file with the following variables:
   ```
   PINECONE_API_KEY=your_pinecone_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Local Development

### Install Dependencies

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

### Run the Backend

```bash
# Activate the virtual environment
poetry shell

# Run the application
poetry run start
```

The API will be available at http://localhost:8000

## API Endpoints

- `GET /`: Welcome message
- `POST /contracts/cron/weekly-embeddings`: Trigger weekly contract embedding generation
- `GET /contracts/test/process-embeddings`: Test endpoint for processing embeddings
- `POST /contracts/search`: Search contracts with a query string

## Deployment

The backend is hosted on Render.com. Deployment is automatic when changes are pushed to the main branch.

### Render Configuration

- **Build Command**: `pip install poetry && poetry install`
- **Start Command**: `poetry run start`
- **Environment Variables**: Set the same variables as in the `.env` file

## How It Works

1. **Contract Scraping**:
   - The system periodically scrapes defense.gov for new contracts
   - Contract data is parsed and structured

2. **Embedding Generation**:
   - Contract text is processed and sent to Google's Gemini API
   - The API returns vector embeddings representing the semantic content
   - These embeddings are stored in Pinecone vector database

3. **Semantic Search**:
   - When a user searches, their query is converted to an embedding
   - This embedding is compared to stored contract embeddings
   - The most semantically similar contracts are returned

## Troubleshooting

- Ensure your API keys are correctly set in the `.env` file
- Check the logs in the `logs/` directory for detailed error information
- Make sure Pinecone index is properly configured with the name "govwatch"
