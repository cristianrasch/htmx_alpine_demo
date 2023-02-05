## [htmx.org](https://htmx.org/docs/) and [alpine.js](https://alpinejs.dev/start-here)
demo app

### Setup

1. Build your containerized env the first time:

`docker-compose build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) --progress plain`

2. Then simply boot up the demo site with:

`docker compose up`

To get rid of the entire setup, simply run this command:

`docker compose down --volumes`

To get rid of the app image run:

```bash
docker rmi htmx_demo-web && docker system prune --force
```
