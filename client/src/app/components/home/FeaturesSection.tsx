"use client";
import React from "react";
import { Zap, ShieldCheck, Feather, LayoutGrid, GitFork } from "lucide-react";
export interface FeatureProps {
    icon: React.ComponentType<any>;
    title: string;
    description: string;
}

const features: FeatureProps[] = [
    {
        icon: Zap,
        title: "FastAPI + Next.js",
        description:
            "Modern full-stack architecture with async Python backend and React frontend.",
    },
    {
        icon: ShieldCheck,
        title: "Authentication Ready",
        description:
            "JWT authentication with secure login, registration, and user management built-in.",
    },
    {
        icon: Feather,
        title: "Type Safety",
        description:
            "Full TypeScript and Python type hints for robust, maintainable code.",
    },
    {
        icon: LayoutGrid,
        title: "Production Ready",
        description:
            "Clean architecture, modern tooling, and deployment-ready configuration.",
    },
];

const Features = () => (
    <section className="py-16 md:py-24 bg-gray-50 dark:bg-gray-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-center text-4xl font-extrabold text-gray-900 dark:text-white">
                Why Choose This Template?
            </h2>
            <p className="mt-4 text-center text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
                Built with modern technologies and best practices for rapid development.
            </p>

            <div className="mt-16 grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4">
                {features.map((feature, index) => (
                    <div
                        key={index}
                        className="p-6 bg-white dark:bg-gray-900 rounded-2xl shadow-xl transition hover:shadow-2xl hover:scale-[1.02] transform duration-300"
                    >
                        {/* The icon components are passed as 'feature.icon' */}
                        <feature.icon className="w-10 h-10 text-indigo-600 dark:text-indigo-400 mb-4" />
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                            {feature.title}
                        </h3>
                        <p className="text-gray-600 dark:text-gray-400">
                            {feature.description}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    </section>
);

export default Features;
