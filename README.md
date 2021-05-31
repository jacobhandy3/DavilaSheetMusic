# DavilaSheetMusic
E-commerce web application to sell sheet music using Django.

## Motivation
This E-commerce project specifically targets sheet music composed by the client. Currently, the client must personally deal with customers, market their product, and provide the products.  This application will handle customers and the products and provide a user-interface for the product to enhance marketability. The client wants to sell his sheet music to customers on a platform where customers can immediately buy and download PDFs of the sheet music.


## Tech/framework used

<b>Built with</b>
- [Python](https://docs.python.org/3/)
- [PostgreSQL](https://www.postgresql.org/docs/13/index.html)
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

## Installation

This project was run on Debian WSL.

<b>Building the Server</b>

It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv -p python3 env
$ source env/bin/activate
$ cd backend
$ pip install -r requirements.txt
$ python3 manage.py runserver
```
