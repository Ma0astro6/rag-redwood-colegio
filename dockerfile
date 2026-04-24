# Usar Python como base
FROM python:3.10-slim

# Crear una carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de tu compu al contenedor
COPY requirements.txt ./
COPY app.py ./

# Instalar las librerías
RUN pip install --no-cache-dir -r requirements.txt

# Decirle a la máquina qué comando ejecutar al inicio
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]