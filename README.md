# jsonbench

Settling an old debate... Using Python/Django, is it more efficient to track
user read posts with a Many to Many database relationship between a User and
the Posts they've read? Or is it more efficient to use a Django Model TextField
to store a JSON object representing a the Posts a User has read?

Let's find out!

## Getting started

Clone this repository and create your virtual environment:

```
jsonbench/$ mkvirtualenv venv
```

Migrate the database (a new sqlite3 db will be created in `db/`):

```
(venv) jsonbench/$ python manage.py migrate
```

Then head into the `scripts/` folder and generate the fixture data that will
populate the database:

```
(venv) jsonbench/$ cd scripts/
(venv) jsonbench/scripts/$ python generate.py
```

Next, load the data:

```
(venv) jsonbench/scripts/$ load_jsonbench.bat
(venv) jsonbench/scripts/$ load_m2mbench.bat
```

Create the superuser:

```
(venv) jsonbench/scripts/$ cd ..
(venv) jsonbench/$ python manage.py createsuperuser
```

Run the server:

```
(venv) jsonbench/$ python manage.py runserver
```

In your browser, head on to http://localhost:8000/admin

Voila!
