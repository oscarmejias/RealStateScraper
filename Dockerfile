FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

# Crear un usuario no root para ejecutar el navegador de forma segura
RUN if ! getent group pwuser > /dev/null 2>&1; then groupadd -r pwuser; fi && \
    if ! getent passwd pwuser > /dev/null 2>&1; then useradd -r -g pwuser -G audio,video pwuser; fi && \
    mkdir -p /home/pwuser/Downloads && \
    chown -R pwuser:pwuser /home/pwuser

WORKDIR /app

# Copiar los archivos del proyecto
COPY requirements.txt .
COPY app.py .
COPY scraper.py .
COPY seccomp_profile.json /home/pwuser/seccomp_profile.json

# Instalar dependencias y configurar Playwright
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium && \
    playwright install-deps && \
    chown -R pwuser:pwuser /app

# Cambiar al usuario no root
USER pwuser

# Exponer el puerto
EXPOSE 8080

# Configurar variables de entorno para Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Comando para ejecutar FastAPI con uvicorn en producción
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4", "--timeout-keep-alive", "120"]
