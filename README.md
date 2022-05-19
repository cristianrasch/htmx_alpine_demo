## [htmx.org](https://htmx.org/docs/) demo app

### Dependencies

* Python 3.10
* Poetry

### Setup

1. Install Python deps with:

```bash
poetry install
```

2. Run demo with:

```bash
FLASK_ENV=development FLASK_APP=app poetry run flask run --with-threads
```
