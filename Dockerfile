FROM python:3.10-slim

# 1. Working directory
WORKDIR /app

# 2. Install system deps (opsiyonel ama genelde iyi)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy project
COPY . .

# 5. Streamlit default port
EXPOSE 8501

# 6. Run Streamlit UI
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.serverAddress=localhost"]
