# FastAPI + Next.js + MongoDB Template - Frontend

Modern Next.js application providing a clean, production-ready frontend foundation with authentication and modern tooling.

## About

This frontend delivers a responsive, type-safe React application with user authentication, API integration, and modern development practices using the latest Next.js and React features.

## Quick Start

```bash
# Install dependencies
npm install

# Copy environment file and configure
cp .env.example .env.local

# Start development server
npm run dev
```

🌐 **Application**: <http://localhost:3000>  
⚡ **Powered by**: Next.js 15 + Turbopack

## Documentation

- 📖 **[Detailed Setup Guide](./INSTALL.md)** - Complete installation instructions
- 🏠 **[Main Project README](../README.md)** - Project overview and full documentation  
- 🔧 **[Backend README](../server/README.md)** - API server setup

## Tech Stack

- **Next.js 15**: React framework with App Router
- **React 19**: Latest React with concurrent features
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Redux Toolkit**: Predictable state management
- **Radix UI**: Accessible component primitives

## Key Features

- Clean, modern UI foundation
- JWT authentication integration
- Responsive design with dark mode support
- Server and client components
- Type-safe API integration
- Production-ready configuration
- Extensible component architecture

## Available Scripts

- `npm run dev` - Development server with Turbopack
- `npm run build` - Production build
- `npm run start` - Production server
- `npm run lint` - Code linting

## Project Structure

```text
client/
├── src/
│   ├── app/             # Next.js App Router
│   │   ├── (auth)/     # Authentication pages
│   │   ├── dashboard/  # Main application
│   │   └── components/ # Page-specific components
│   ├── components/     # Reusable React components
│   │   ├── ui/        # Base UI components (shadcn/ui)
│   │   └── layout/    # Layout components
│   ├── hooks/         # Custom React hooks
│   ├── lib/           # Utilities and API client
│   ├── store/         # Redux store configuration
│   └── types/         # TypeScript type definitions
├── public/            # Static assets
└── INSTALL.md        # Detailed setup guide
```

## Contributing

Please refer to the main project [README](../README.md) for contribution guidelines.
