# Learning-Management-System

## General Info

Learning Management System is a software that can be used by universities for assignments, grading and resource sharing. It covers both the sides viz. faculties and students. Features for creating posts, grading and resource sharing have been provided on both the ends.

## Technology Stack
Front End: Django
Back End: Django
Language: Python
Database: SQLite
Software Engineering Process Model: Agile
Software Engineering Methodology: Scrum

## Installation Process

1. Clone this repository

Use the following command to clone this repository
```
git clone https://github.com/nancyradadia/Learning-Management-System
```

2. Install the requirements

Navigate into the src folder and use the following command to install all the required packages
```
pip install -r requirements.txt
```

3. Set up the database

Use the following commands to setup migrations

```
python manage.py makemigrations
python manage.py migrate
```

4. Start the application

Django application can be started by the following command

```
python manage.py runserver
```

5. Go to the following URL to see the site running at localhost

```
http://127.0.0.1:8000/
```


## Requirements:
```shell
pip install django-session-timeout
pip install django-livereload-server
```


---
**NOTE**

The database is already preconfigured and has some content in it. The credentials for admin are:

email: admin@gmail.com  
password: admin12345

---
