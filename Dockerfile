FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ❌ EXPOSE hata do (optional)
# EXPOSE 8000

# ✅ ONLY THIS (MOST IMPORTANT LINE)
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port $PORT"]
