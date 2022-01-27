# Grupo R5 - API Books

<p align="center">
  <a href="https://www.grupor5.com"><img src="https://user-images.githubusercontent.com/34389493/150956700-2e070ea3-8d05-4e6a-bda5-972f2a431dfb.png" alt="GroupR5"></a>
</p>
<p align="center">
    <em>Grupo R5 - API Books</em>
</p>


## Introduction
API Books es un proyecto de evaluación propuesto por Grupo R5 que comprende las funcionalidades y microservicios para el procesamiento y disponibilización de libros por medio de repositorios internos y/o externos(Google Books y OpenLibra)

## Getting Started
1. pre requirements
  OS: Linux - Ubuntu <optional>
3.	Installation process
```bash
pip3 install virtualenv
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements/development.txt

# to deactivate venv
deactivate
```
### Run

```bash
python manage.py
```

## Build and Test
### Install Requirements Test
```bash
pip install -r requirements/test.txt
```
### Run Test
```bash
pytest -vs test
```
### Run Test and Coverage
```bash
pytest -v --cov src --cov-report html test
```
### Run Test and Coverage include file .coveragerc
```bash
pytest -v --cov src --cov-report html --cov-config=.coveragerc test
```

## Documentations
- [`Swagger`](http://ec2-18-229-245-105.sa-east-1.compute.amazonaws.com:5000/docs)
- [`Redocs`](http://ec2-18-229-245-105.sa-east-1.compute.amazonaws.com:5000/redoc)
- extra docs: views ./docs/
  
## Usage Example
- [`GET Books`](http://ec2-18-229-245-105.sa-east-1.compute.amazonaws.com:5000/books/?author=david)
  curl --location --request GET 'http://ec2-18-229-245-105.sa-east-1.compute.amazonaws.com:5000/books/?author=david'
-- Nota: Filtros validos para GET Books (id, title, subtitle, author, category, datetime_publication, editor, description)
- [`DELETE Book`] curl --location --request DELETE 'http://ec2-18-229-245-105.sa-east-1.compute.amazonaws.com:5000/books/?id=book3'
