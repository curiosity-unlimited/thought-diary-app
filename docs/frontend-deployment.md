# Frontend Deployment

This document describes how to deploy the Thought Diary App frontend to production environments.

## Table of Contents
- [Overview](#overview)
- [Build Process](#build-process)
- [Environment Configuration](#environment-configuration)
- [Static Hosting Platforms](#static-hosting-platforms)
- [CDN Deployment](#cdn-deployment)
- [Docker Deployment](#docker-deployment)
- [Performance Optimization](#performance-optimization)
- [Monitoring and Analytics](#monitoring-and-analytics)
- [Troubleshooting](#troubleshooting)

## Overview

The frontend is a single-page application (SPA) built with Vue 3 and Vite. It compiles to static assets that can be served from any static hosting platform or CDN.

**Deployment Options:**
- **Static Hosting**: Netlify, Vercel, GitHub Pages, AWS S3
- **CDN**: Cloudflare, AWS CloudFront, Azure CDN
- **Container**: Docker with Nginx
- **Traditional**: VPS with Nginx

**Requirements:**
- Node.js 18+ (for build)
- Modern web server (for serving static files)
- HTTPS certificate
- Backend API endpoint

## Build Process

### Production Build

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

**Output:**
- Built files in `frontend/dist/`
- Optimized and minified JavaScript/CSS
- Source maps for debugging (optional)

### Build Configuration

**vite.config.ts:**
```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath, URL } from 'node:url';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false, // Enable for debugging
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.logs
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
        },
      },
    },
  },
});
```

### Build Optimization

**Enable Source Maps (Development Only):**
```typescript
build: {
  sourcemap: true,
}
```

**Code Splitting:**
```typescript
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ['vue', 'vue-router', 'pinia'],
        ui: ['@headlessui/vue', 'vue-toastification'],
        utils: ['axios', 'yup', 'vee-validate'],
      },
    },
  },
}
```

**Remove Console Logs:**
```typescript
build: {
  minify: 'terser',
  terserOptions: {
    compress: {
      drop_console: true,
      drop_debugger: true,
    },
  },
}
```

## Environment Configuration

### Production Environment Variables

Create `.env.production`:

```bash
# API Configuration
VITE_API_BASE_URL=https://api.thoughtdiary.com

# App Information
VITE_APP_NAME=Thought Diary
VITE_APP_VERSION=0.1.0
```

**Important:**
- All variables must start with `VITE_`
- Variables are baked into build at build time
- Never include secrets in environment variables
- Use different `.env.production` for different environments

### Environment-Specific Builds

```bash
# Production build
npm run build

# Staging build
npm run build -- --mode staging

# Custom environment
npm run build -- --mode custom
```

**Create `.env.staging`:**
```bash
VITE_API_BASE_URL=https://staging-api.thoughtdiary.com
VITE_APP_NAME=Thought Diary (Staging)
```

## Static Hosting Platforms

### Netlify

**1. Deploy via Git**

Create `netlify.toml` in project root:

```toml
[build]
  base = "frontend/"
  command = "npm run build"
  publish = "dist/"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"

[context.production.environment]
  VITE_API_BASE_URL = "https://api.thoughtdiary.com"

[context.staging.environment]
  VITE_API_BASE_URL = "https://staging-api.thoughtdiary.com"
```

**2. Connect Repository**
- Go to https://app.netlify.com
- Click "Add new site" → "Import an existing project"
- Connect GitHub repository
- Configure build settings (auto-detected from netlify.toml)
- Deploy

**3. Configure Custom Domain**
- Go to Site settings → Domain management
- Add custom domain
- Configure DNS records
- Enable HTTPS (automatic with Netlify)

**Environment Variables:**
- Go to Site settings → Environment variables
- Add `VITE_API_BASE_URL`
- Deploy to apply changes

### Vercel

**1. Deploy via Git**

Create `vercel.json` in project root:

```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "devCommand": "cd frontend && npm run dev",
  "installCommand": "cd frontend && npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

**2. Connect Repository**
- Go to https://vercel.com
- Click "Add New" → "Project"
- Import Git repository
- Configure root directory: `frontend/`
- Deploy

**3. Environment Variables**
- Go to Project Settings → Environment Variables
- Add `VITE_API_BASE_URL` for Production
- Add separate values for Preview/Development
- Redeploy to apply changes

### GitHub Pages

**1. Install gh-pages**

```bash
npm install --save-dev gh-pages
```

**2. Configure package.json**

```json
{
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  },
  "homepage": "https://username.github.io/thought-diary-app"
}
```

**3. Configure vite.config.ts**

```typescript
export default defineConfig({
  base: '/thought-diary-app/', // Repository name
  // ... other config
});
```

**4. Deploy**

```bash
npm run deploy
```

**Note:** GitHub Pages doesn't support SPA routing by default. Add `404.html` redirect:

```html
<!-- dist/404.html -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Thought Diary</title>
    <script>
      sessionStorage.redirect = location.href;
    </script>
    <meta http-equiv="refresh" content="0;URL='/thought-diary-app'"></meta>
  </head>
  <body></body>
</html>
```

### AWS S3 + CloudFront

**1. Create S3 Bucket**

```bash
aws s3 mb s3://thoughtdiary-frontend
aws s3 website s3://thoughtdiary-frontend --index-document index.html --error-document index.html
```

**2. Upload Build**

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://thoughtdiary-frontend --delete
```

**3. Configure Bucket Policy**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::thoughtdiary-frontend/*"
    }
  ]
}
```

**4. Create CloudFront Distribution**

```bash
aws cloudfront create-distribution \
  --origin-domain-name thoughtdiary-frontend.s3.amazonaws.com \
  --default-root-object index.html
```

**5. Configure Custom Error Pages**

CloudFront → Error Pages → Create Custom Error Response:
- HTTP Error Code: 403, 404
- Response Page Path: /index.html
- HTTP Response Code: 200

## CDN Deployment

### Cloudflare

**1. Add Site to Cloudflare**
- Sign up at https://cloudflare.com
- Add your domain
- Update nameservers at domain registrar

**2. Configure DNS**
```
Type: CNAME
Name: @
Target: your-netlify-site.netlify.app
Proxy: Enabled (Orange cloud)
```

**3. Enable Performance Features**
- Go to Speed → Optimization
- Enable Auto Minify (JS, CSS, HTML)
- Enable Brotli compression
- Enable Rocket Loader (optional)

**4. Configure Cache Rules**
- Go to Caching → Configuration
- Cache Level: Standard
- Browser Cache TTL: 4 hours
- Always Online: Enabled

**5. Page Rules**
```
URL: *thoughtdiary.com/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
  - Browser Cache TTL: 4 hours
```

### AWS CloudFront

See AWS S3 section above for CloudFront setup.

**Cache Behavior Settings:**
```
Path Pattern: *
Compress Objects: Yes
Viewer Protocol Policy: Redirect HTTP to HTTPS
Allowed HTTP Methods: GET, HEAD, OPTIONS
Cache Policy: CachingOptimized
Origin Request Policy: AllViewer
```

**Invalidation After Deployment:**
```bash
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

## Docker Deployment

### Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# Production stage
FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### Nginx Configuration

Create `frontend/nginx.conf`:

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        VITE_API_BASE_URL: ${VITE_API_BASE_URL}
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Build and Run

```bash
# Build image
docker build \
  --build-arg VITE_API_BASE_URL=https://api.thoughtdiary.com \
  -t thoughtdiary-frontend:latest \
  ./frontend

# Run container
docker run -d \
  -p 80:80 \
  --name thoughtdiary-frontend \
  thoughtdiary-frontend:latest

# Or use docker-compose
docker-compose up -d
```

### Docker Registry

**Push to Docker Hub:**
```bash
docker tag thoughtdiary-frontend:latest username/thoughtdiary-frontend:latest
docker push username/thoughtdiary-frontend:latest
```

**Push to AWS ECR:**
```bash
aws ecr create-repository --repository-name thoughtdiary-frontend

docker tag thoughtdiary-frontend:latest \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/thoughtdiary-frontend:latest

docker push \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/thoughtdiary-frontend:latest
```

## Performance Optimization

### Asset Optimization

**1. Image Optimization**
- Use WebP format where supported
- Provide multiple sizes for responsive images
- Lazy load images below the fold
- Use SVG for icons and logos

**2. Code Splitting**
```typescript
// Route-based splitting (already configured)
const Dashboard = () => import('@/views/Dashboard.vue');

// Component-based splitting
const HeavyComponent = defineAsyncComponent(
  () => import('@/components/HeavyComponent.vue')
);
```

**3. Tree Shaking**
```typescript
// ✅ Good: Import specific functions
import { ref, computed } from 'vue';

// ❌ Bad: Import entire library
import * as Vue from 'vue';
```

**4. Bundle Analysis**
```bash
npm install --save-dev rollup-plugin-visualizer
```

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    vue(),
    visualizer({ open: true }),
  ],
});
```

### Caching Strategy

**1. Cache-Control Headers**

```nginx
# nginx.conf
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location ~* \.(html)$ {
    expires -1;
    add_header Cache-Control "no-cache, no-store, must-revalidate";
}
```

**2. Service Worker (Future)**

```javascript
// service-worker.js
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open('thoughtdiary-v1').then((cache) => {
      return cache.addAll([
        '/',
        '/index.html',
        '/assets/index.js',
        '/assets/index.css',
      ]);
    })
  );
});
```

### Loading Performance

**1. Preload Critical Assets**

```html
<!-- index.html -->
<head>
  <link rel="preload" href="/assets/index.js" as="script">
  <link rel="preload" href="/assets/index.css" as="style">
</head>
```

**2. DNS Prefetch**

```html
<head>
  <link rel="dns-prefetch" href="https://api.thoughtdiary.com">
</head>
```

**3. Lazy Loading**

```vue
<template>
  <img src="image.jpg" loading="lazy" alt="Description">
</template>
```

## Monitoring and Analytics

### Error Tracking

**Sentry Integration:**

```bash
npm install @sentry/vue
```

```typescript
// src/main.ts
import * as Sentry from '@sentry/vue';

Sentry.init({
  app,
  dsn: 'YOUR_SENTRY_DSN',
  integrations: [
    new Sentry.BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
    }),
  ],
  tracesSampleRate: 1.0,
  environment: import.meta.env.MODE,
});
```

### Performance Monitoring

**Google Analytics:**

```html
<!-- index.html -->
<head>
  <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'GA_MEASUREMENT_ID');
  </script>
</head>
```

**Web Vitals:**

```bash
npm install web-vitals
```

```typescript
// src/main.ts
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

### Health Checks

**Nginx Health Endpoint:**

```nginx
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}
```

**Test:**
```bash
curl http://your-domain.com/health
```

## Troubleshooting

### Common Issues

**Issue: Blank Page After Deployment**

**Possible Causes:**
1. Incorrect base URL in vite.config.ts
2. Missing SPA routing configuration
3. CORS errors from API

**Solutions:**
```typescript
// vite.config.ts - Check base URL
export default defineConfig({
  base: '/', // Or '/subdirectory/' for subdirectory deployment
});
```

```nginx
# nginx.conf - Ensure SPA routing
location / {
    try_files $uri $uri/ /index.html;
}
```

**Issue: API Calls Failing**

**Check:**
1. `VITE_API_BASE_URL` environment variable
2. CORS configuration on backend
3. Network tab in browser DevTools

**Solution:**
```bash
# Verify environment variable in build
echo $VITE_API_BASE_URL

# Check backend CORS settings
# backend/config.py should allow frontend origin
```

**Issue: Assets Not Loading**

**Check:**
1. Base URL configuration
2. Asset paths in build
3. CDN/cache invalidation

**Solution:**
```bash
# View build output
ls -la frontend/dist/assets/

# Clear CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id ID \
  --paths "/*"
```

**Issue: 404 on Refresh**

**Cause:** Server not configured for SPA routing

**Solution:**
```nginx
# nginx.conf
location / {
    try_files $uri $uri/ /index.html;
}
```

For Netlify:
```toml
# netlify.toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Rollback Strategy

**1. Version Tagging**
```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

**2. Deployment Snapshots**
- Keep previous build artifacts
- Use deployment platform's rollback feature
- Maintain deployment history

**3. Quick Rollback**
```bash
# Netlify
netlify deploy --prod --dir=previous-dist/

# AWS S3
aws s3 sync previous-dist/ s3://bucket/ --delete

# Docker
docker run previous-image:tag
```

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy-frontend.yml`:

```yaml
name: Deploy Frontend

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci
      - name: Run tests
        working-directory: ./frontend
        run: npm run test:coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          directory: ./frontend/coverage

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        working-directory: ./frontend
        run: npm ci
      - name: Build
        working-directory: ./frontend
        env:
          VITE_API_BASE_URL: ${{ secrets.VITE_API_BASE_URL }}
        run: npm run build
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v2
        with:
          publish-dir: './frontend/dist'
          production-deploy: true
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

## Related Documentation

- [Frontend Development](./frontend-development.md) - Development setup and workflow
- [Frontend Architecture](./frontend-architecture.md) - Architecture patterns
- [Backend Deployment](./backend-deployment.md) - Backend deployment guide
- [Frontend Testing](./frontend-testing.md) - Testing before deployment
