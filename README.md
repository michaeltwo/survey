# Survey Management System

This is an survey management system for TDS Final Project

Running Environment: Python 3.12.5, django 5.1.1, postgresql 16.4, MS-win11 local tested

## Installation

Prerequsites: python, django, pipenv(optional). make sure port 8000(web),5432(sql) are free.

Installation steps as below:
 - For python installation, if you are using linux, just using apt install(debain), yum install python(redhat). If you are using windows, just download the package form <https://www.python.org/downloads/>, and install it.
 - For django and pipenv, steps as below
 
```bash
pip install pipenv
pip install django
```
After all installtion done. open a cmd command, and input below commands to check the if environment are good to run.
Make sure django is running by type below command, if version number shows, then you are good to go
>python --version

>django-admin --version

(optional), if you want to run code in pipenv, you should start a pipenv shell to create a virtual environment.

Then go below steps:

1. git clone https://github.com/michaeltwo/survey.git
unzip and copy files into a folder and cd to the survey_group8 folder, for example c:\

```bash
cd c:\survey_group8
```
2. setup database connections, create a database and update the database settings in settings.py

edit c:\survey_group8\survey_group8\settings.py, as below:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'testdb', #use the database name you created
        'USER': 'postgres', #database username
        'PASSWORD': 'password', #database password
        'HOST': 'localhost',  # Set to the DB server IP if using a remote DB
        'PORT': '5432',        # Default PostgreSQL port
    }
}
```
3. run django migration to create tables in postgres database
```bash
cd c:\survey_group8
python manage.py makemigrations
python manage.py migrate
```

4. run server using below command
>python manage.py runserver

5. if it is running locally, just open a web brower and type in <http://127.0.0.1:8000>

   if it is running in a server, please input the server ip address <http://serverIP:8000>

## Usage

1. register a user, if you already have an account, can perform login directly

2. survey taker and survey craeter

3. click on logout, after operate done. 

NOTE. Remember your username and password


## Contributing

Please let us know if any confusion, 

Group: 8

Group Members: Michael Fasching, Weihua Zheng, Dev Shah, Shubham Ganesh Junnarkar

## License
This is just for TDS Final Project
Author: Michael F, Michael Z, Dev S, Shubham G J

[MIT](https://choosealicense.com/licenses/mit/)

[Django](https://docs.djangoproject.com/zh-hans/5.0/py-modindex/)
