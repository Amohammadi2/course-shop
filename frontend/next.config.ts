
import {hostname} from 'os';

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/register/',
        destination: 'http://127.0.0.1:8000/api/register/',
      },
      {
        source: '/api/auth/token/',
        destination: 'http://127.0.0.1:8000/api/auth/token/',
      },
      {
        source: '/api/me/',
        destination: 'http://127.0.0.1:8000/api/me/',
      },
    ]
  },
};

export default nextConfig;
