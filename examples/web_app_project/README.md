# Web Application Project

A full-stack web application with React frontend and Flask backend, demonstrating modern web development practices.

## Project Structure

```
web_app_project/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   └── services/        # API service layer
│   └── package.json
├── backend/                 # Flask backend API
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   └── requirements.txt    # Python dependencies
├── database/               # Database related files
│   ├── migrations/         # SQL migration files
│   └── seeds/             # Sample data
├── docs/                   # Project documentation
│   ├── API_DOCUMENTATION.md
│   └── DEPLOYMENT_GUIDE.md
├── tests/                  # Test files
│   └── test_api.py
└── docker-compose.yml      # Docker orchestration
```

## Features

- **Frontend**: React 18 with modern hooks and component architecture
- **Backend**: Flask REST API with SQLAlchemy ORM
- **Database**: PostgreSQL with migration support
- **Authentication**: JWT-based authentication (planned)
- **Testing**: Comprehensive unit and integration tests
- **Deployment**: Docker containerization with multi-service setup
- **Documentation**: Complete API documentation and deployment guides

## Quick Start

1. **Using Docker (Recommended)**:
   ```bash
   docker-compose up -d
   ```

2. **Manual Setup**:
   
   Backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
   
   Frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```

## API Endpoints

- `GET /api/users/{id}` - Get user by ID
- `POST /api/users` - Create new user
- `GET /api/metrics/{user_id}` - Get user metrics
- `POST /api/metrics` - Create new metric

## Technology Stack

- **Frontend**: React, CSS3, Modern JavaScript (ES6+)
- **Backend**: Python, Flask, SQLAlchemy
- **Database**: PostgreSQL, Redis (for caching)
- **DevOps**: Docker, Docker Compose
- **Testing**: Jest (frontend), unittest (backend)

## Development

- Follow the API documentation in `docs/API_DOCUMENTATION.md`
- See deployment instructions in `docs/DEPLOYMENT_GUIDE.md`
- Run tests with `npm test` (frontend) or `python -m unittest` (backend)

## License

MIT License - feel free to use this project as a foundation for your own applications.
