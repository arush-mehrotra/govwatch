# GovWatch

GovWatch is a modern web application that brings transparency to government contract spending through AI-powered search and data visualization.

![GovWatch Logo](frontend/public/logo.png)

## Project Overview

GovWatch makes government contract data accessible to everyone through:

- **Natural Language Search**: Ask questions in plain English about government contracts
- **Automated Data Collection**: Regular scraping of defense.gov contract announcements
- **AI-Powered Analysis**: Vector embeddings and semantic search to find relevant contracts
- **User-Friendly Interface**: Clean, responsive design that works on all devices

## Repository Structure

This monorepo contains both the frontend and backend components:

```
govwatch/
├── frontend/           # Next.js frontend application
│   ├── app/            # Pages and layouts
│   ├── components/     # Reusable UI components
│   └── ...
├── backend/            # FastAPI backend application
│   ├── app/            # API code
│   │   ├── routes/     # API endpoints
│   │   ├── services/   # Business logic
│   │   └── ...
│   └── ...
└── ...
```

## Getting Started

### Prerequisites

- Node.js 18.x+ (frontend)
- Python 3.11+ (backend)
- Poetry (Python dependency management)
- Pinecone account (vector database)
- Google Gemini API key

### Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

### Running the Backend

```bash
cd backend
poetry install
poetry run start
```

The backend API will be available at http://localhost:8000

## Environment Setup

### Frontend Environment

Create a `.env.local` file in the frontend directory:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend Environment

Create a `.env` file in the backend directory:

```
PINECONE_API_KEY=your_pinecone_api_key
GEMINI_API_KEY=your_gemini_api_key
```

## Deployment

- **Frontend**: Deployed on Vercel
- **Backend**: Deployed on Render.com

## Architecture

GovWatch uses a modern architecture:

1. **Data Collection**:
   - Python scraper collects contract data from defense.gov
   - Data is processed and structured

2. **Vector Embeddings**:
   - Contract text is converted to vector embeddings using Google's Gemini API
   - Embeddings are stored in Pinecone vector database

3. **Search API**:
   - FastAPI backend provides endpoints for searching contracts
   - User queries are converted to embeddings and compared with stored contract embeddings

4. **Frontend**:
   - Next.js application provides a user-friendly interface
   - Communicates with the backend API to retrieve search results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or feedback, please open an issue on this repository.
