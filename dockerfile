# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Environment vars ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- Default database settings for Docker ----------
ENV POSTGRES_SERVER=db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=user_management

# ---------- Work directory ----------
WORKDIR /app

# ---------- System deps for psycopg2 ----------
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev \
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