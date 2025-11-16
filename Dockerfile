# Dockerfile para Sistema de Análisis de Emergencias - Ventanilla
# Basado en Python 3.12 oficial

FROM python:3.12-slim

# Metadata
LABEL maintainer="Nik Denilson"
LABEL description="Sistema de Análisis de Llamadas de Emergencia con Clustering K-means"
LABEL version="2.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para matplotlib y pandas
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app_mejorado.py .
COPY static/ ./static/
COPY templates/ ./templates/

# Crear directorio para resultados si no existe
RUN mkdir -p static

# Exponer puerto 5000 (Flask)
EXPOSE 5000

# Variables de entorno para Flask
ENV FLASK_APP=app_mejorado.py \
    FLASK_ENV=production \
    FLASK_DEBUG=0

# Comando de inicio
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]

