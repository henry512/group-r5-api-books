FROM python:3.8.5-slim-buster

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install wheel && pip install -r requirements/production.txt

EXPOSE 5000
CMD ["python", "manage.py"]