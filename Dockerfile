# Используем официальный образ Python
FROM python:3.9-slim

# Установка зависимостей для Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends

# Установка Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Установка ChromeDriver
ARG CHROME_DRIVER_VERSION=114.0.5735.90
RUN wget -q https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && rm chromedriver_linux64.zip

# Рабочая директория
WORKDIR /app

# Копирование файлов
COPY app/requirements.txt .
COPY app/main.py .
COPY app/chromedriver /usr/local/bin/chromedriver

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска
CMD ["python", "main.py"]