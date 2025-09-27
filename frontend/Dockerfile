FROM node:18.18-alpine3.18

WORKDIR /app

# Install dependencies first
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Then copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Install serve
RUN npm install -g serve

EXPOSE 3000

# Use serve to run the built application
CMD ["serve", "-s", "build", "-l", "3000"]