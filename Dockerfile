FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

WORKDIR /home/pwuser/app

# Copiar los archivos del proyecto
COPY --chown=pwuser:pwuser requirements.txt .
COPY --chown=pwuser:pwuser app.py .
COPY --chown=pwuser:pwuser scraper.py .
COPY --chown=pwuser:pwuser seccomp_profile.json .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorio para screenshots
RUN mkdir -p /home/pwuser/app/screenshots && \
    chown -R pwuser:pwuser /home/pwuser/app/screenshots

# Cambiar al usuario no root
USER pwuser

# Exponer el puerto (Railway asignará el puerto automáticamente)
EXPOSE 8080

# Variables de entorno para optimizar el uso de memoria
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
ENV PLAYWRIGHT_BROWSER_EXECUTABLE_PATH=/ms-playwright/chromium-*/chrome-linux/chrome
# Limitar el uso de memoria de Node.js a 307MB (60% de 512MB disponible)
ENV NODE_OPTIONS="--max-old-space-size=307"
ENV PLAYWRIGHT_HEADLESS_MODE=1
ENV PLAYWRIGHT_BROWSERS_ONLY=1
# Variable para Railway
ENV PORT=8080

# Comando recomendado para ejecutar FastAPI con uvicorn en producción
# Reducido el número de workers debido a la memoria limitada
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
