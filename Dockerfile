FROM python:3.10-slim

# ishchi papka
WORKDIR /app

# tizim kutubxonalarini o‘rnatish (PDF va docx uchun zarur)
RUN apt-get update && apt-get install -y \
    libmagic-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# python kutubxonalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# loyihani nusxalash
COPY . .

# .env o‘qilishi uchun
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
