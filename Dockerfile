FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Inicia o servidor gunicorn, e usa a porta definida em PORT(Se houver) ou 8000 como porta padrão
CMD ["sh", "-c", "exec gunicorn wsgi:app --bind 0.0.0.0:${PORT:-8000}"]  # 'sh -c' inicia um Shell para interpretar o comando '${PORT:-8000}'
