FROM node:18.18-alpine3.18 AS builder

WORKDIR /app

# Add necessary build tools
RUN apk add --no-cache python3 make g++ git

# Copy package files
COPY package*.json ./
COPY .npmrc ./

# Install dependencies with optimizations
RUN npm config set fetch-retry-maxtimeout 600000 \
    && npm config set fetch-retry-mintimeout 100000 \
    && npm cache clean --force \
    && npm install --legacy-peer-deps \
        --prefer-offline \
        --no-audit \
        --no-fund \
        --max-old-space-size=4096 \
        --network-timeout=600000

# Copy source
COPY . .

# Build with environment variables
ENV NODE_ENV=production
ENV DISABLE_ESLINT_PLUGIN=true
ENV GENERATE_SOURCEMAP=false
RUN npm run build

# Production image
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Add nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]