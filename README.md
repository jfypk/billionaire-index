# Billionaire Impact Ranking System

A comprehensive platform for tracking and analyzing billionaire impact across social, environmental, political, philanthropic, and cultural dimensions. The system aggregates data from multiple authoritative sources and incorporates public sentiment to provide transparent, data-driven rankings.

## System Architecture

### Components

1. **FastAPI Backend**
   - REST API endpoints for rankings, voting, and reporting
   - JWT-based authentication
   - Background tasks for data updates

2. **Data Collection System**
   - Web scrapers for multiple sources:
     - OpenSecrets (Political influence)
     - ProPublica (Tax practices, philanthropy)
     - CDP (Climate and environmental impact)
     - SEC (Corporate governance)
     - Glassdoor (Worker treatment)

3. **PostgreSQL Database**
   - Stores billionaire profiles and scores
   - Public sentiment weightings
   - User-submitted reports and evidence

4. **Scoring Algorithm**
   - Dynamic weighting system based on public votes
   - Categories:
     - Social Impact (30%)
     - Environmental Responsibility (20%)
     - Political Influence (20%)
     - Philanthropy (20%)
     - Cultural Impact (10%)

## Development Setup

### Prerequisites

1. Python 3.11
2. PostgreSQL database
3. Required API keys (will be prompted during setup)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd billionaire-impact-ranking
```

2. Install dependencies:
```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary python-jose trafilatura
```

3. Set up environment variables:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/billionaire_ranking"
```

4. Initialize the database:
```bash
alembic upgrade head
```

### Running the Development Server

Start the FastAPI server:
```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

## API Documentation

### Endpoints

- `GET /rankings`: Get ranked list of billionaires
- `GET /billionaire/{id}`: Get individual billionaire data
- `POST /vote`: Submit weight adjustments for scoring categories
- `POST /report`: Submit evidence about a billionaire
- `POST /update-data/{billionaire_id}`: Trigger data update for a specific billionaire
- `POST /update-all-data`: Trigger data update for all billionaires

### Authentication

The API uses JWT tokens for authentication:
1. Get token: `POST /token`
2. Use token in Authorization header: `Bearer <token>`

## Database Schema

### Tables

1. `billionaires`
   - Core metrics and scores
   - Overall ranking calculations

2. `votes`
   - Public sentiment weightings
   - Category importance votes

3. `reports`
   - User-submitted evidence
   - Verification status

## Deployment

### Replit Deployment

1. Fork the project on Replit
2. Set up environment secrets:
   - `DATABASE_URL`
   - API keys for data sources (will be prompted)

3. Run the deployment:
   - The system will automatically use port 5000
   - Replit will handle SSL/TLS and domain configuration

### Production Considerations

1. Data Updates
   - Configure scheduled tasks for regular data collection
   - Monitor rate limits for data sources

2. Database Migrations
   - Use Alembic for schema changes
   - Test migrations in staging environment

3. Security
   - Rotate JWT secrets regularly
   - Monitor API rate limits
   - Validate user-submitted content

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with:
   - Clear description of changes
   - Test coverage
   - Documentation updates

## License

[Add your license information here]
