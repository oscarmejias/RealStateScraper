FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

WORKDIR /app

# Copiar los archivos del proyecto
COPY requirements.txt .
COPY app.py .
COPY scraper.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"] 