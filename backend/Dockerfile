# Imagen de DESARROLLO del backend: simple a propósito (sin multi-stage ni optimizaciones).
FROM python:3.13-slim

# uv con la versión fijada en el TRD §1
RUN pip install --no-cache-dir uv==0.13.5

# El entorno virtual vive en /opt/venv (fuera de /app) para que el código montado
# como volumen en docker-compose no lo tape.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# 1) Dependencias exactas del uv.lock
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# 2) Código de la API
COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
