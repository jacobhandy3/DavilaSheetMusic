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

1. Install Linux or [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
2. Update and Upgrade packages
```sh
$ sudo apt-get update
$ sudo apt-get upgrade
```
3. Install [Python](https://medium.com/@rhdzmota/python-development-on-the-windows-subsystem-for-linux-wsl-17a0fa1839d) and [virtualenv](https://pythonbasics.org/virtualenv/)
4. Clone the repository (specific branch)
```sh
$ git clone --branch [branch name] [git url]
```

It is best to use the python `virtualenv` tool to build locally:

```sh
$ cd [repository folder]
$ virtualenv -p python3 env
$ source env/bin/activate
$ cd backend
$ pip install -r requirements.txt
$ cd backend
#Generate a settings.py here
#Setup a database with Django
$ python3 manage.py runserver
```

Done! You are ready to start contributing!