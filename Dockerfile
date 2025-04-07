FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

# Crear un usuario no root
RUN useradd -m -u 1000 pwuser && \
    mkdir -p /home/pwuser/app && \
    chown -R pwuser:pwuser /home/pwuser

WORKDIR /home/pwuser/app

# Copiar los archivos del proyecto
COPY --chown=pwuser:pwuser requirements.txt .
COPY --chown=pwuser:pwuser app.py .
COPY --chown=pwuser:pwuser scraper.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorio para screenshots
RUN mkdir -p /home/pwuser/app/screenshots && \
    chown -R pwuser:pwuser /home/pwuser/app/screenshots

# Cambiar al usuario no root
USER pwuser

# Exponer el puerto
EXPOSE 8080

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Comando recomendado para ejecutar FastAPI con uvicorn en producción
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
