# Deployment Guide

## Prerequisites

- Docker and Docker Compose
- PostgreSQL database
- Node.js 18+ for frontend
- Python 3.9+ for backend

## Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/webapp_db

# Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Redis (for rate limiting)
REDIS_URL=redis://localhost:6379
```

## Docker Deployment

1. Build and run with Docker Compose:

```bash
docker-compose up -d
```

2. Run database migrations:

```bash
docker-compose exec backend python -c "from app import db; db.create_all()"
```

## Manual Deployment

### Backend Deployment

1. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2. Set environment variables:

```bash
export DATABASE_URL=postgresql://username:password@localhost:5432/webapp_db
export SECRET_KEY=your-secret-key-here
export FLASK_ENV=production
```

3. Run database migrations:

```bash
python -c "from app import db; db.create_all()"
```

4. Start the application:

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

### Frontend Deployment

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Build for production:

```bash
npm run build
```

3. Serve static files with nginx or similar.

## Monitoring

- Application logs are available via `docker-compose logs`
- Database performance can be monitored using PostgreSQL's built-in tools
- Consider setting up application monitoring with tools like Sentry or New Relic

## Security Considerations

- Use HTTPS in production
- Regularly update dependencies
- Implement proper authentication and authorization
- Use environment variables for sensitive configuration
- Enable database connection pooling
- Set up proper backup procedures
