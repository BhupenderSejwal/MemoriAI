FROM python:3.10-slim

# 1. Working directory
WORKDIR /app

# 2. Install system dependencies (optional but helpful)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy project
COPY . .

# 5. Streamlit port
EXPOSE 8000 8501

# 6. Run Streamlit UI
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
#CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]