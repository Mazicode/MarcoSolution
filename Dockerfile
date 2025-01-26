FROM python:3.9-slim

WORKDIR /app

# Set the PYTHONPATH to ensure Python can find modules in /app
ENV PYTHONPATH=/app:$PYTHONPATH

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
