## [htmx.org](https://htmx.org/docs/) and [alpine.js](https://alpinejs.dev/start-here)
demo app

### Dependencies

* Python 3.10
* Poetry
* direnv (optional)

### Setup

1. Install Python deps with:

```bash
poetry install
```

2. Run demo with:

```bash
FLASK_DEBUG=1 FLASK_APP=app poetry run flask run --with-threads
```

or if you are a direnv user you can streamline that process somewhat by:

```bash
direnv allow
poetry run flask run --with-threads
```

### If you want to use Docker & docker-compose instead..

1. Build your containerized env the first time:

`docker-compose build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) --progress plain`

2. Then simply boot up the demo site with:

`docker-compose up`

To get rid of the entire setup, simply run this command:

`docker-compose down --volumes`

To get rid of the app image run:

```bash
docker rmi htmx_demo_web && docker system prune --force
```
