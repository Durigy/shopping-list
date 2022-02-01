# flask-shopping-list
This is a shopping list webapp built in flask/python without JS

-----------------------------------

Python version: 3.10.1

### Required set up configurations:

It is good practice to create a virtual environment for the project
this can be done in the folder root folder using the following windows (or equivalent) terminal commands

    > py -m venv venv

    > venv\Scripts\activate

    > py -m pip install -r requirements.txt

> note: if you do not activate the venv before installing the requirements.txt,
> then it will be installed in your main python directory

-----------------------------------------------------

In-order to connect to a database either create a file in ./shop/ called 'config.py'
this must contain the folowing variables (shown using mysql):

```python
secret_key = '<- add secret key here ->' 

database_uri = 'mysql+pymysql://<- DB Password ->@<- DB domain/IP (localhost normally) ->/<- DB Name ->'

debug_setting = <- True or False ->
```

> replace the <- -> with the correct info

or

#### change the config settings to something more relevant

app.config['SECRET_KEY'] = **db_var.SECRET_KEY**

app.config['SQLALCHEMY_DATABASE_URI'] = **db_var.SQLALCHEMY_DATABASE_URI**

-----------------------------------------------------

### Secret key generation  
Use the following python commands to generate a secret key:

    > python

    >>> import os

    >>> os.urandom(24).hex()

-----------------------------------------------------

### To add the tables to your local testing database, for example
you can use the following commands:

    > python

    >>> from main import db

    >>> db.create_all()

-----------------------------------------------------

# Images of the Site
## Login Page
![login-page](https://user-images.githubusercontent.com/56241583/152062367-efe23946-1bc2-46b6-8821-e612dc8be094.JPG)

## Account Page
![account-page](https://user-images.githubusercontent.com/56241583/152062179-d7cb640f-1502-4fc7-a898-d1d6fd6def77.JPG)

## View all Shopping Lists
![user-view-all-lists](https://user-images.githubusercontent.com/56241583/152062421-db38bc7b-1dff-4a01-a2cd-39a6f7a1b586.JPG)

## Add item in Shopping List
![adding-item-to-list](https://user-images.githubusercontent.com/56241583/152062530-d23942cc-5be5-4c27-b177-5b776c83a366.JPG)

## Edit item in Shopping List
![editing-item](https://user-images.githubusercontent.com/56241583/152062496-7acef8b2-8adc-4301-b886-85525fe6cd81.JPG)

## Delete item in Shopping List
![deleting-item-from-list](https://user-images.githubusercontent.com/56241583/152062571-2207f312-c3c6-4d39-af53-ad64925bc643.JPG)

