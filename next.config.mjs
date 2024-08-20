/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
            {
                source: "/api/:path*",
                destination: "http://127.0.01:8080/:path*"
            }
        ]
    }
};

export default nextConfig;
