FROM python:3.11-slim

WORKDIR /app

RUN useradd --create-home appuser
USER appuser

COPY --chown=appuser:appuser requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--workers","1"]
