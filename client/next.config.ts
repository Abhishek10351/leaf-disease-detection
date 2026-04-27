import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    images: {
        remotePatterns: [
            {
                protocol: "http",
                hostname: "localhost",
                port: "8000",
                pathname: "/analysis/images/**",
            },
        ],
    },
    allowedDevOrigins: ["127.0.0.1"],
};

export default nextConfig;
