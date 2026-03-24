# Build frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Final image
FROM python:3.11-slim
WORKDIR /app

# Install Node.js in the Python image
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Copy and install backend dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy everything
COPY . .

# Copy frontend build from builder
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/node_modules ./frontend/node_modules

# Ensure scripts are executable
RUN chmod +x start.sh

# Default environment variables
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

# The start.sh handles both backend and frontend
CMD ["/bin/bash", "./start.sh"]
