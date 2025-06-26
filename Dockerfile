# Bazaviy Python image
FROM python:3.12

# Ishchi katalog
WORKDIR /app

# Requirements
COPY requirements.txt .

# Paketlarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Appni ko‘chirish
COPY . .

# Port ochish
EXPOSE 8000

# FastAPI serverni ishga tushurish
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
