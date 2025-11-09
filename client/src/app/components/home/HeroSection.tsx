import { GitFork, Code, Database } from "lucide-react";

const Hero = () => {
    return (
        <section className="min-h-screen bg-white dark:bg-gray-900 flex items-center justify-center py-24">
            <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
                {/* Badge */}
                <span className="inline-block px-4 py-2 mb-8 text-sm font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 rounded-full">
                    Full-Stack Template
                </span>

                {/* Main Heading */}
                <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
                    FastAPI + Next.js
                    <span className="block text-blue-600 dark:text-blue-400">
                        MongoDB Template
                    </span>
                </h1>

                {/* Subheading */}
                <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-12 max-w-3xl mx-auto">
                    Production-ready full-stack template with FastAPI backend,
                    Next.js frontend, and MongoDB database. Authentication, API
                    docs, and modern tooling included.
                </p>

                {/* Tech Stack Icons */}
                <div className="flex justify-center items-center gap-8 mb-12">
                    <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
                        <Code className="w-5 h-5" />
                        <span className="text-sm font-medium">FastAPI</span>
                    </div>
                    <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
                        <span className="text-sm font-medium">Next.js</span>
                    </div>
                    <div className="flex items-center gap-2 text-gray-600 dark:text-gray-300">
                        <Database className="w-5 h-5" />
                        <span className="text-sm font-medium">MongoDB</span>
                    </div>
                </div>

                {/* CTAs */}
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <a
                        href="#"
                        className="inline-flex items-center justify-center px-8 py-3 text-base font-medium rounded-lg 
                                  bg-blue-600 text-white hover:bg-blue-700 
                                  transition-colors duration-200"
                    >
                        Get Started
                    </a>
                    <a
                        href="https://github.com/Abhishek10351/fastapi-nextjs-mongo-template"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center justify-center px-8 py-3 text-base font-medium rounded-lg 
                                  border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 
                                  hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200"
                    >
                        <GitFork className="w-4 h-4 mr-2" />
                        View on GitHub
                    </a>
                </div>
            </div>
        </section>
    );
};

export default Hero;
