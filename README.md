# legislation reader

This Django app is part of the tutorial on using the Laws.Africa Content API.

For more details, see the Laws.Africa developer guide at https://developers.laws.africa/

## Getting started

Clone this repo and `cd` into the repo directory.

Install and activate a python environment:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Run the local server:

```
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.
