# GovWatch Frontend

A modern, responsive web application built with Next.js that provides an intuitive interface for searching and exploring government contract data.

## Overview

The GovWatch frontend is a static Next.js application that will connect to our FastAPI backend to provide users with a powerful search interface for government contract data. The application uses modern web technologies to create a responsive and accessible user experience.

## Tech Stack

- **Framework**: [Next.js](https://nextjs.org/) (React framework)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Language**: TypeScript
- **Deployment**: Vercel

## Project Structure

```
frontend/
├── app/                  # Next.js app directory (pages and layouts)
│   ├── about/            # About page
│   ├── page.tsx          # Home page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/           # Reusable UI components
│   └── ui/               # UI component library
├── lib/                  # Utility functions and shared code
├── public/               # Static assets
└── ...config files       # Various configuration files
```

## Getting Started

### Prerequisites

- Node.js 18.x or later
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

### Development

Run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Connecting to the Backend

The frontend is designed to connect to our FastAPI backend. To connect to the backend:

1. The backend API is hosted at `https://govwatch.onrender.com` in production
2. For local development, the backend should be running at `http://localhost:8000`

To configure the API endpoint, you can set the `NEXT_PUBLIC_API_URL` environment variable:

```bash
# For local development
NEXT_PUBLIC_API_URL=http://localhost:8000

# For production
NEXT_PUBLIC_API_URL=https://govwatch.onrender.com
```

## API Integration

The frontend will communicate with the backend through the following endpoints:

- `POST /contracts/search` - Search for contracts using natural language queries
- Additional endpoints will be added as the application evolves

## Deployment

The frontend is deployed on Vercel. The deployment process is automated through GitHub integration:

1. Push changes to the main branch
2. Vercel automatically builds and deploys the application
3. The live site is updated with the new changes

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Submit a pull request

## Future Development

- Add authentication for admin users
- Implement advanced filtering options
- Create data visualization components
- Add export functionality for search results
