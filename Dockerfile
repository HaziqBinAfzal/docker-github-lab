FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 labuser
COPY app.py .
USER labuser
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --start-period=10s --retries=6 \
    CMD python -c "import json,urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=2); assert r.status == 200 and json.load(r) == {'status':'ok'}"
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
