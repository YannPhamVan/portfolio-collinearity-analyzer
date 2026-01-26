# Stage 1: Build Frontend
FROM node:20-alpine as build-frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Unified Backend
FROM python:3.12-slim

WORKDIR /app

# Copy backend requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY backend/ /app/backend/

# Copy Frontend Build to backend/static
# We place it inside /app/backend/static so that uvicorn running from /app/backend sees it?
# Wait, we run uvicorn from /app usually?
# In backend/Dockerfile we did:
# WORKDIR /app
# COPY backend/ . (contents of backend to /app)
# CMD ["uvicorn", "main:app"...]

# Let's replicate that structure for consisteny
COPY backend/ .
COPY --from=build-frontend /app/build /app/static

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
