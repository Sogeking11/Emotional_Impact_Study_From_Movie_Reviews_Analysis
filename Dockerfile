FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
#CMD [ "python", "./main.py" ]