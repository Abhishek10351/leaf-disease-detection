# 🌿 Leaf Disease Detection AI

An advanced AI-powered plant disease detection and care recommendation system built with modern web technologies and cutting-edge machine learning capabilities.

![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?style=for-the-badge&logo=fastapi)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-47A248?style=for-the-badge&logo=mongodb)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google)

## 🚀 Technical Features

### 🧠 AI-Powered Analysis

- **Modular AI Provider Architecture**: Extensible system supporting multiple AI providers (Gemini, OpenAI, Claude, etc.)
- **LangChain Integration**: Uses industry-standard LangChain for consistent AI model interfaces
- **Multi-Modal Support**: Vision and text analysis capabilities across different AI providers
- **Intelligent Provider Fallback**: Automatic failover between providers for maximum reliability
- **Structured JSON Responses**: Advanced prompt engineering returns structured data with user-friendly summaries and detailed technical analysis
- **Intelligent Content Parsing**: Robust JSON parsing with fallback to markdown format for reliability
- **Dynamic Severity Assessment**: Automatic extraction of disease severity levels and care difficulty ratings
- **Mock Mode**: Complete testing capabilities without requiring API keys

### 🖥️ Modern Frontend Architecture

- **Next.js 15**: Latest React framework with App Router and TypeScript support
- **shadcn/ui Components**: Beautiful, accessible UI components with consistent design system
- **Tailwind CSS**: Modern utility-first CSS framework with custom theming
- **Dark Mode Support**: Complete dark/light theme with proper color schemes
- **Responsive Design**: Mobile-first approach with adaptive layouts

### ⚙️ Backend Excellence

- **FastAPI**: High-performance Python web framework with automatic OpenAPI documentation
- **Modular AI Service Architecture**: Clean separation between AI providers and business logic
- **Provider Registry System**: Dynamic registration and management of AI providers
- **Health Monitoring**: Real-time monitoring of AI provider availability and performance
- **Proper HTTP Semantics**: RESTful API design with appropriate status codes (2xx, 4xx, 5xx)
- **File Storage System**: Efficient image storage with metadata tracking in MongoDB
- **Async Operations**: Non-blocking file operations with aiofiles
- **Pydantic Models**: Type-safe data validation and serialization
- **Comprehensive Testing**: Unit, integration, and performance tests with mocking support

### 📊 Rich Content Display

- **Markdown Rendering**: React Markdown with syntax highlighting using rehype-highlight
- **Structured Information Cards**: Color-coded sections for immediate actions, treatments, and prevention
- **Visual Hierarchy**: Emojis, badges, and proper spacing for enhanced readability
- **Progressive Disclosure**: Quick summaries for casual users, detailed analysis for experts

### 🎨 User Experience Features

- **Three Analysis Types**:
  - Image-based plant disease detection
  - Symptom description analysis
  - Comprehensive plant care guides
- **Interactive Components**: Tabbed interface with history tracking
- **Real-time Feedback**: Loading states, progress indicators, and error handling
- **Actionable Results**: Copy and print functionality for care instructions

## 🚀 Quick Start

### Prerequisites

- **Python** 3.11+ and **uv** (or pip)
- **Node.js** 18+ and **npm**
- **MongoDB** 4.4+ (local or cloud)
- **Google Gemini API Key**
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/Abhishek10351/leaf-disease-detection.git
cd leaf-disease-detection
```

### 2. Backend Setup

```bash
cd server

# Install dependencies
uv sync
# or with pip
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings (especially GEMINI_API_KEY)

# Start backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
cd client

# Install dependencies
npm install

# Start development server
npm run dev
```

**Available URLs:**

- Frontend: <http://localhost:3000>
- Backend API: <http://localhost:8000>
- API Documentation: <http://localhost:8000/docs>

## 📁 Project Structure

```text
leaf-disease-detection/
├── client/                    # Next.js Frontend ✅
│   ├── src/
│   │   ├── app/              # App Router pages
│   │   │   ├── page.tsx      # Home page
│   │   │   ├── analysis/     # Analysis dashboard
│   │   │   └── globals.css   # Global styles
│   │   ├── components/       # React components
│   │   │   ├── ui/          # shadcn/ui components
│   │   │   └── analysis/    # Analysis-specific components
│   │   ├── lib/             # Utilities and services
│   │   ├── types/           # TypeScript type definitions
│   │   └── styles/          # Additional styles
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── server/                   # FastAPI Backend ✅
│   ├── app/
│   │   ├── api/             # API routes
│   │   │   └── analysis/    # Analysis endpoints
│   │   ├── core/            # Core configuration
│   │   ├── models/          # Pydantic models
│   │   ├── db/              # Database operations
│   │   ├── llm_core/        # AI integration
│   │   └── utils/           # Utility functions
│   ├── uploads/             # File storage
│   │   └── images/          # Uploaded images
│   ├── .env                 # Backend environment
│   └── requirements.txt     # Backend dependencies
└── README.md               # This file
```

> **Status**: ✅ Full-Stack Application Ready

## 🏗️ AI Provider Architecture

The system uses a modular AI provider architecture that makes it easy to support multiple AI services:

### 🔧 Base Provider System

```python
class AIProvider(ABC):
    """Base class with complete analysis implementations"""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.llm = self._initialize_llm()  # LangChain model
    
    @abstractmethod
    def _initialize_llm(self):
        """Only method providers need to implement"""
        pass
    
    # Complete implementations included:
    def analyze_image(self, image_base64: str, context: str = "") -> Dict[str, Any]:
        """✅ Complete implementation using LangChain"""
    
    def analyze_symptoms(self, symptoms: str, plant_type: str = None) -> Dict[str, Any]:
        """✅ Complete implementation using LangChain"""
    
    def get_care_tips(self, plant_type: str) -> Dict[str, Any]:
        """✅ Complete implementation using LangChain"""
```

### 🔌 Adding New Providers

Adding a new AI provider requires minimal code:

```python
# 1. Create provider class
class ClaudeProvider(AIProvider):
    def _initialize_llm(self):
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=self.model_name,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )

# 2. Register in system
ai_service.register_provider(ProviderType.CLAUDE, ClaudeProvider())
```

### 🛡️ Automatic Features

Every provider automatically gets:
- ✅ **Mock Mode**: Works without API keys for testing
- ✅ **Error Handling**: Graceful fallback to mock responses  
- ✅ **JSON Parsing**: Robust response parsing with fallback
- ✅ **Health Checks**: Automatic provider monitoring
- ✅ **Consistent Interface**: Same methods across all providers

### 🔄 Provider Management

```python
# Service manager handles multiple providers
ai_service = AIServiceManager()

# Register providers
ai_service.register_provider(ProviderType.GEMINI, GeminiProvider())
ai_service.register_provider(ProviderType.OPENAI, OpenAIProvider())

# Set active provider with automatic fallback
ai_service.set_active_provider(ProviderType.GEMINI)
ai_service.set_fallback_providers([ProviderType.OPENAI])

# All analysis calls automatically use active provider with fallback
result = ai_service.analyze_image("base64_image")
```

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

### Image Analysis

- `POST /api/analysis/images/upload` - Upload plant image
- `POST /api/analysis/images/analyze` - Analyze uploaded image
- `GET /api/analysis/images/{image_id}/view` - View uploaded image

### Symptoms Analysis

- `POST /api/analysis/symptoms` - Analyze plant symptoms from description

### Care Tips

- `POST /api/analysis/care` - Get comprehensive plant care guidelines

### Utility

- `GET /ping` - Health check

### Example Requests

#### Image Analysis

```bash
# Upload image
curl -X POST "http://localhost:8000/api/analysis/images/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@plant_image.jpg"

# Analyze image
curl -X POST "http://localhost:8000/api/analysis/images/analyze" \
  -H "Content-Type: application/json" \
  -d '{"image_id": "your-image-id"}'
```

#### Symptoms Analysis

```bash
curl -X POST "http://localhost:8000/api/analysis/symptoms" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms_description": "Yellow spots on leaves with brown edges",
    "plant_type": "Tomato"
  }'
```

## 🌐 Environment Variables

### Backend (server/.env)

```bash
# Required
GEMINI_API_KEY=your-google-gemini-api-key
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=leaf_disease_detection

# Optional
PROJECT_NAME="Leaf Disease Detection AI"
ENVIRONMENT=development
BACKEND_CORS_ORIGINS=http://localhost:3000
UPLOAD_DIR=uploads
MAX_FILE_SIZE_MB=10
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Getting API Keys

1. **Google Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new project or use existing one
   - Generate an API key for Gemini models
   - Add to your `.env` file as `GEMINI_API_KEY`

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

## 🎯 Key Innovations

### 1. **Dual-Content Strategy**

- Quick, actionable summaries for immediate use
- Detailed technical analysis for in-depth understanding
- Progressive disclosure based on user needs

### 2. **Structured AI Responses**

- JSON-first approach with markdown fallback
- Consistent field extraction across different analysis types
- User-friendly language with technical accuracy

### 3. **Visual Information Architecture**

- Color-coded sections for different information types
- Emoji-enhanced headers for quick scanning
- Card-based layout for mobile-friendly consumption

### 4. **Professional Development Practices**

- Type-safe development with TypeScript and Pydantic
- Modern tooling with UV, Next.js, and Tailwind
- Clean architecture with separation of concerns

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

- Check the [Issues](https://github.com/Abhishek10351/leaf-disease-detection/issues) page
- Review the API documentation at `/docs` when running locally
- Consult the inline code documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for powerful AI capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python web framework
- [Next.js](https://nextjs.org/) for the modern React framework
- [shadcn/ui](https://ui.shadcn.com/) for beautiful, accessible components
- [MongoDB](https://www.mongodb.com/) for flexible document storage
- [Tailwind CSS](https://tailwindcss.com/) for utility-first styling

---

## 🌿 Happy Plant Care

Built with ❤️ by [Abhishek10351](https://github.com/Abhishek10351)
