# VYAS Vedic Yield Astrology Systems - Production Dockerfile
FROM python:3.11-slim

# Install system dependencies & Google Chrome for HarfBuzz PDF publication engine
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    fonts-noto-core \
    fonts-noto-extra \
    fonts-deva \
    ca-certificates \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

ENV PORT=8501
ENV HOST=0.0.0.0

CMD ["python", "run_web_terminal.py"]
