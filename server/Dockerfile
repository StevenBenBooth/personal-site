FROM python:3.10

COPY src/ /app
WORKDIR /app

RUN pip install --upgrade pip
# warns you to create a user and venv, even in container. I'm going to ignore it 
RUN pip install -r requirements.txt

# gcloud expects this
ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app