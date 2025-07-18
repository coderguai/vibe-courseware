# Vibe Courseware

A modern courseware management system built with FastAPI, SQLModel, and Alembic.

## Features

- RESTful API with FastAPI
- Database ORM with SQLModel
- Database migrations with Alembic
- Environment-based configuration
- Structured project layout

## Project Structure

```
vibe-courseware/
├── .env                  # Environment variables (not in git)
├── .env.example          # Example environment variables
├── .gitignore            # Git ignore file
├── .python-version       # Python version file
├── alembic.ini           # Alembic configuration
├── migrations/           # Database migrations
├── pyproject.toml        # Project configuration
├── README.md             # Project documentation
├── run.py                # Entry point script
├── src/                  # Source code
│   └── vibe_courseware/  # Main package
│       ├── api/          # API endpoints
│       ├── config/       # Configuration
│       ├── db/           # Database
│       ├── models/       # Data models
│       ├── services/     # Business logic
│       └── utils/        # Utilities
└── tests/                # Tests
    ├── integration/      # Integration tests
    └── unit/             # Unit tests
```

## Development

### Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies: `uv pip install -e ".[dev]"`
5. Copy `.env.example` to `.env` and adjust settings if needed

### Run the Application

```bash
python run.py
```

The API will be available at http://localhost:8000

### Database Migrations

Create a migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

### Testing

```bash
pytest
```

## License

MIT