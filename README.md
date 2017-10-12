# jsonbench

Settling an old debate... Using Python/Django, is it more efficient to track
user read posts with a Many to Many database relationship between a User and
the Posts they've read? Or is it more efficient to use a Django Model TextField
to store a JSON object representing a the Posts a User has read?

Let's find out!

## Getting started

Clone this repository and create your virtual environment:

```
$ cd /path/to/folder
$ git clone https://github.com/jonmsawyer/jsonbench.git
$ cd jsonbench/
jsonbench/$ mkvirtualenv venv
```

Install project requirements:

```
(venv) jsonbench/$ pip install -r requirements.txt
```

Migrate the database (a new sqlite3 db will be created in `db/`):

```
(venv) jsonbench/$ python manage.py migrate
```

Create the superuser:

```
(venv) jsonbench/$ python manage.py createsuperuser
```

Then head into the `scripts/` folder and generate the fixture data that will
populate the database:

```
(venv) jsonbench/$ cd scripts/
(venv) jsonbench/scripts/$ python generate.py
```

Next, load the generated fixture data.

On Windows:

```
(venv) jsonbench/scripts/$ load_jsonbench.bat
(venv) jsonbench/scripts/$ load_m2mbench.bat
```

On \*Nix:

```
(venv) jsonbench/scripts/$ ./load_jsonbench.sh
(venv) jsonbench/scripts/$ ./load_m2mbench.sh
```

> **Please wait while this loads the generated fixture data, this could take a while. Now's a great time to get a coffee :)**

Randomly "read" the forum posts, passing in the `username` of the superuser you created:

```
(venv) jsonbench/scripts/$ python read_posts.py myusername
```

> **Please wait while this reads the posts, this could take a while. Now's a great time to get more coffee :)**


Run the server:

```
(venv) jsonbench/scripts/$ cd ..
(venv) jsonbench/$ python manage.py runserver
```

In your browser, head on to http://localhost:8000/admin

Voila!
