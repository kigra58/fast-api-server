# ---------- Base image ----------
    FROM python:3.11-slim

    # ---------- Environment vars ----------
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1 \
        PIP_NO_CACHE_DIR=1
    
    # ---------- Default database settings for Docker (development only) ----------
    # Provide real secrets at runtime or through docker-compose/CI/CD.
    ENV POSTGRES_SERVER=db \
        POSTGRES_USER=postgres \
        POSTGRES_PASSWORD=postgres \
        POSTGRES_DB=user_management
    
    # ---------- Work directory ----------
    WORKDIR /app
    
    # ---------- System deps for psycopg2 ----------
    RUN apt-get update && apt-get install -y --no-install-recommends \
            build-essential \
            libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    # ---------- Python deps ----------
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # ---------- App code ----------
    COPY . .
    
    # ---------- Expose FastAPI port ----------
    EXPOSE 8000
    
    # ---------- Start command ----------
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    