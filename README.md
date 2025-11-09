# 🚀 FastAPI + Next.js + MongoDB Template

A modern, production-ready full-stack template featuring FastAPI backend and Next.js frontend with MongoDB database. Complete with authentication, type safety, and best practices built-in.

![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-47A248?style=for-the-badge&logo=mongodb)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python)

## ✨ Features

### 🔐 Authentication & Security

- **JWT Authentication**: Secure token-based authentication
- **User Management**: Complete user registration and profile management
- **Password Security**: bcrypt hashing for secure password storage
- **CORS Protection**: Configurable cross-origin request handling

### 🚀 Backend Foundation

- **FastAPI**: Modern async Python web framework
- **Database**: MongoDB with async operations
- **Authentication**: JWT tokens with secure implementation
- **Validation**: Pydantic for data validation and serialization

### 🎨 Frontend (Coming Soon)

- **Next.js 15**: React framework with App Router
- **React 19**: Latest React with concurrent features
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Redux Toolkit**: State management
- **Radix UI**: Accessible component primitives

### 📊 Developer Experience

- **Type Safety**: Full TypeScript and Python type hints
- **Auto Documentation**: OpenAPI/Swagger docs generated automatically
- **Hot Reload**: Fast development with auto-reload
- **Code Quality**: Ruff for backend, ESLint for frontend
- **Testing**: Pytest for backend, Jest for frontend
- **Environment Management**: Clean configuration management

## 🚀 Quick Start

### Prerequisites

- **Python** 3.12+ and **uv** (or pip)
- **Node.js** 18+ and **npm** (for upcoming frontend)
- **MongoDB** 4.4+ (local or cloud)
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/Abhishek10351/fastapi-nextjs-mongo-template.git
cd fastapi-nextjs-mongo-template
```

### 2. Environment Setup

Configure your backend environment:

```bash
cd server
cp .env.example .env
# Edit server/.env with your backend settings
```

**Required changes:**

- Change `SECRET_KEY` from "changethis" to a secure random string
- Change `FIRST_SUPERUSER_PASSWORD` from "changethis" to a secure password
- Update `MONGODB_URI` if using a different MongoDB setup

### 3. Backend Setup

```bash
cd server

# Install dependencies
uv sync

# Start backend server
cd app
fastapi dev main.py
```

Backend will be available at: <http://localhost:8000>

- API Docs: <http://localhost:8000/docs>
- Alternative Docs: <http://localhost:8000/redoc>

## 📁 Project Structure

```text
fastapi-nextjs-mongo-template/
├── client/                # Next.js Frontend (Coming Soon)
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks
│   │   ├── lib/         # Utilities and API
│   │   └── store/       # Redux store
│   ├── public/          # Static assets
│   ├── .env.local       # Frontend environment
│   └── INSTALL.md       # Frontend setup guide
├── server/               # FastAPI Backend ✅
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core functionality
│   │   ├── models.py    # Data models
│   │   ├── db/          # Database operations
│   │   └── utils/       # Utility functions
│   ├── .env             # Backend environment
│   └── INSTALL.md       # Backend setup guide
└── README.md           # This file
```

> **Status**: ✅ Backend Ready | 🚧 Frontend Coming Soon

## 🛠️ Development

### Backend Commands (Available Now)

```bash
# Development server (from app/ directory)
cd app && fastapi dev main.py

# Production server
cd app && uv run fastapi run app/main.py

# Run tests
uv run pytest

# Code linting and formatting
uv run ruff check
uv run ruff format
```

### Frontend Commands (Coming Soon)

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## 🔗 API Endpoints

### Authentication

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### Users

- `GET /users/me` - Get user profile
- `PUT /users/me` - Update profile

### Utility

- `GET /ping` - Health check

> **Note**: Add your own business logic endpoints here. The template provides a solid foundation with authentication and user management.

## 🌐 Environment Variables

### Backend (server/.env)

```bash
# Required
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=your_app_name
SECRET_KEY=your-secret-key
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=secure-password

# Optional
PROJECT_NAME="Your App Name"
ACCESS_TOKEN_EXPIRE_MINUTES=11520  # 8 days
ENVIRONMENT=local
BACKEND_CORS_ORIGINS=http://localhost:3000
```

## 🧪 Testing

### Backend Tests (Available Now)

```bash
cd server
uv run pytest                 # Run all tests
uv run pytest --cov=app      # With coverage
uv run pytest -v             # Verbose output
```

### Frontend Tests (Coming Soon)

```bash
cd client
npm run test                  # Run tests
npm run test:watch           # Watch mode
npm run test:coverage        # With coverage
```

## 🚀 Deployment

### Production Environment

1. **Set production environment variables**
2. **Use production MongoDB instance**
3. **Configure HTTPS and security headers**
4. **Set up monitoring and logging**

### Deployment Options

- **Docker**: Use provided Dockerfiles
- **Cloud Platforms**: Vercel (frontend), Railway/Render (backend)
- **VPS**: Nginx + PM2/systemd
- **Container Orchestration**: Kubernetes

## 🔒 Security Features

- JWT token authentication with 8-day expiration
- bcrypt password hashing
- CORS protection
- Input validation with Pydantic
- Environment-based configuration
- Secure HTTP headers

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure all tests pass and code is formatted
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Development Setup

1. Follow the Quick Start guide above
2. Install development dependencies
3. Run tests to ensure everything works
4. Make your changes
5. Test your changes thoroughly

## 📚 Documentation

- [Backend Installation Guide](./server/INSTALL.md)
- [Frontend Installation Guide](./client/INSTALL.md) (Coming Soon)
- [API Documentation](http://localhost:8000/docs) (when running)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [MongoDB Documentation](https://www.mongodb.com/docs/)

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Ensure MongoDB is running: `mongosh --eval "db.runCommand('ping')"`
   - Check connection string in .env file

2. **Port Already in Use**
   - Backend: `lsof -i :8000` and kill the process
   - Frontend: `lsof -i :3000` and kill the process

3. **Environment Variables Not Loading**
   - Ensure .env file is in the correct location
   - Restart development servers after changes

4. **JWT Token Issues**
   - Change SECRET_KEY to a secure random string
   - Clear browser storage and re-login

### Getting Help

- Check the [Issues](https://github.com/Abhishek10351/fastapi-nextjs-mongo-template/issues) page
- Review the installation guide in `/server/INSTALL.md`
- Join our community discussions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing Python web framework
- [Next.js](https://nextjs.org/) for the excellent React framework (coming soon)
- [MongoDB](https://www.mongodb.com/) for the flexible document database
- [Pydantic](https://docs.pydantic.dev/) for data validation and settings management

---

## 🚀 Happy Building

Made with ❤️ by [Abhishek10351](https://github.com/Abhishek10351)