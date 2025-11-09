# FastAPI + Next.js + MongoDB Template - Backend

FastAPI backend server providing secure REST APIs with authentication, user management, and extensible architecture.

## About

This backend provides a robust foundation for full-stack applications with JWT authentication, MongoDB integration, and auto-generated API documentation. Ready to extend with your own business logic.

## Quick Start

```bash
# Install dependencies
uv sync

# Copy environment file and configure
cp .env.example .env

# Initialize database
uv run python -m app.initial_data

# Start development server
cd app && fastapi dev main.py
```

🌐 **API Server**: <http://localhost:8000>  
📚 **API Docs**: <http://localhost:8000/docs>

## Documentation

- 📖 **[Detailed Setup Guide](./INSTALL.md)** - Complete installation instructions
- 🏠 **[Main Project README](../README.md)** - Project overview and full documentation

## Tech Stack

- **FastAPI**: Modern async Python web framework
- **MongoDB**: Document database with async operations  
- **JWT**: Secure token-based authentication
- **Pydantic**: Data validation and serialization
- **bcrypt**: Password hashing

## API Features

- User authentication and registration
- JWT token management with refresh
- Auto-generated OpenAPI documentation
- Async database operations
- Type-safe request/response handling
- Extensible architecture for custom endpoints

## Project Structure

```text
server/
├── app/
│   ├── api/routes/      # API endpoints
│   ├── core/           # Configuration & security
│   ├── models/         # MongoDB data models
│   ├── crud/           # Database operations
│   ├── schemas/        # Pydantic schemas
│   └── main.py        # Application entry point
├── pyproject.toml     # Dependencies & config
└── INSTALL.md        # Detailed setup guide
```

## Contributing

Please refer to the main project [README](../README.md) for contribution guidelines.