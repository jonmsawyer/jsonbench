# jsonbench

Settling an old debate... Using Python/Django, is it more efficient to track
user read posts with a Many to Many database relationship between a User and
the Posts they've read? Or is it more efficient to use a Django Model TextField
to store a JSON object representing the Posts a User has read?

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

Generate fixture data for the apps you're interested in benchmarking:

```
(venv) jsonbench/$ python manage.py jsondictbench_generate
(vent) jsonbench/$ python manage.py m2mbench_generate
```

Load the generated fixture data.

```
(venv) jsonbench/$ python manage.py jsondictbench_load
(vent) jsonbench/$ python manage.py m2mbench_load
```

> **Please wait while this loads the generated fixture data, this could take a while.
> Now's a great time to get a coffee :)**

Randomly "read" the forum posts, passing in the `username` of the superuser you created:

```
(venv) jsonbench/$ python manage.py jsondictbench_read_posts
(vent) jsonbench/$ python manage.py m2mbench_read_posts
```

> **Please wait while this reads the posts, this could take a while.
> Now's a great time to get more coffee :)**

Run the server:

```
(venv) jsonbench/scripts/$ cd ..
(venv) jsonbench/$ python manage.py runserver 8000
```

In your browser, head on over to http://localhost:8000/ for web benchmarking,
head on over to http://localhost:8000/admin/ for for the Django Admin.

Voila!
