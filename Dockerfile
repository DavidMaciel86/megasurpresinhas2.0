FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação
COPY src ./src

# Copia os arquivos responsáveis por iniciar a aplicação
COPY wsgi.py .
COPY run.py .

# Permite ao Python localizar o pacote dentro da estrutura src
ENV PYTHONPATH=/app/src

EXPOSE 8000

# Inicia o Gunicorn usando PORT(Se houver) ou 8000 como valor padrão
CMD ["sh", "-c", "exec gunicorn wsgi:app --bind 0.0.0.0:${PORT:-8000}"]
