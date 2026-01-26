FROM python:3.12-slim

WORKDIR /app

# Copy requirement file first to leverage cache
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
# Since the Dockerfile is inside backend/ we copy . to /app
# But wait, the previous instructions assumed Dockerfile in root or backend/ 
# Standard pattern: Context is usually root.
# Let's assume build context is project root as per README instructions:
# docker build -t portfolio-backend -f backend/Dockerfile .

# If context is root:
COPY backend/ backend/
# We also need imports to work. The app runs from /app usually.
# If we run `uvicorn backend.main:app` from /app, it works if backend is a package.
# Or we can WORKDIR /app/backend

# Let's follow the README instructions which said:
# COPY backend/ .
# This implies context is root and we copy backend folder into /app (so /app/backend/...) or contents?
# A clearer approach for the user's previous README snippet:
# WORKDIR /app
# COPY backend/ .  -> This copies backend contents to /app? No, "COPY src dest".
# If dest is ., it copies to WORKDIR.

# Let's stick to a robust standard:
# Dockerfile will be in backend/Dockerfile.
# Build context will be root.

COPY backend/ /app/backend/
# Also need requirements.

# Let's adjust slightly to be safe and simple.
# If we copy everything to /app, we can run uvicorn from there.

# Re-reading README instructions I wrote:
# WORKDIR /app
# COPY backend/ . 
# This implies we copy backend/* to /app/. so /app/main.py exists.

COPY backend/ .

# Expose port
EXPOSE 8000

# Command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
