FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# 🔧 system dependencies (important for numpy, opencv, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 📦 upgrade pip (VERY IMPORTANT)
RUN pip install --upgrade pip

# 📥 install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📁 copy project
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
