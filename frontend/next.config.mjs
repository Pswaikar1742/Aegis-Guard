/** @type {import('next').NextConfig} */
const nextConfig = {
  // This flag will skip TypeScript type-checking during the `next build` command.
  typescript: {
    ignoreBuildErrors: true,
  },
  // This flag will skip ESLint checks during the `next build` command.
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;