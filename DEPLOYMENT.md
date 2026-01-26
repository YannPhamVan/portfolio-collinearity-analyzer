# Deployment Guide

Since the application is containerized with a **Unified Dockerfile** at the root, deployment is straightforward on platforms that support Docker.

## Option 1: PaaS (Easiest - Render, Railway, Fly.io)
These platforms connect directly to your GitHub repository, detect the `Dockerfile`, and build/deploy automatically.

### **Render.com** (Recommended)

#### Method A: Blueprints (Automated)
1.  Push your code to GitHub.
2.  In Render Dashboard, click **New** -> **Blueprint**.
3.  Connect your repository.
4.  Render will auto-detect `render.yaml` and configure everything (Docker, Region, Port).
5.  Click **Apply**.

#### Method B: Manual Setup
1.  Push your code to GitHub.
2.  Create a new **Web Service** on Render.
3.  Connect your repository.
4.  **Runtime**: Select `Docker`.
5.  **Region**: Choose closest to you (e.g., Frankfurt).
6.  **Plan**: Free tier works (but sleeps after inactivity). Basic plan ($7/mo) avoids cold starts.
7.  Click **Create Web Service**.
    *   Render will build the image (Node build -> Python setup).
    *   It will expose port `8000` automatically (or you can set `PORT` env var to 8000).

### **Railway.app**
1.  Login and "New Project" -> "Deploy from GitHub repo".
2.  Railway detects the `Dockerfile` automatically.
3.  It will build and deploy.
4.  Go to Settings -> Generate Domain to get a public URL.

## Option 2: Serverless Containers (Google Cloud Run)
Great for scaling and paying only for usage.

1.  **Install Google Cloud SDK**.
2.  **Build & Push** image to Google Container Registry (GCR):
    ```bash
    gcloud builds submit --tag gcr.io/PROJECT_ID/portfolio-analyzer
    ```
3.  **Deploy**:
    ```bash
    gcloud run deploy portfolio-analyzer \
      --image gcr.io/PROJECT_ID/portfolio-analyzer \
      --platform managed \
      --port 8000 \
      --allow-unauthenticated
    ```

## Option 3: VPS (DigitalOcean, AWS EC2, Hetzner)
Manual control on a Linux server.

1.  **Provision a server** (Ubuntu).
2.  **Install Docker**:
    ```bash
    apt update && apt install docker.io -y
    ```
3.  **Clone & Run**:
    ```bash
    git clone https://github.com/YOUR_USER/repo.git
    cd repo
    docker build -t app .
    docker run -d -p 80:8000 --restart always app
    ```
    *Note: Maps port 80 (HTTP) to container's 8000.*

## Important Notes
-   **Environment Variables**: If you add API keys later (e.g., for a paid data provider), set them in the dashboard of your cloud provider.
-   **Database**: Currently, the app uses `yfinance` (no DB) and mocked data. It is stateless, so "Scale to Zero" (Cloud Run) works perfectly.
