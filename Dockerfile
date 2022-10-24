# syntax=docker/dockerfile:1.3
FROM python:3.10-bullseye AS builder

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN python -m pip install --upgrade pip
ENV REQUIREMENTS_FILE=requirements.txt
COPY $REQUIREMENTS_FILE .
ENV PATH=/root/.local/bin:$PATH
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir --user -r $REQUIREMENTS_FILE

FROM python:3.10-slim-bullseye

ARG USER_ID=1000
ARG GROUP_ID=1000

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENV USR=dev GRP=dev APP_DIR=/usr/src/app

RUN apt-get update -qq \
  && apt-get upgrade -qq \
  && apt-get install -yq --no-install-recommends \
    netcat \
  && apt-get clean \
  && rm -rf /var/cache/apt/archives/* \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
  && truncate -s 0 /var/log/*log

RUN addgroup --gid $GROUP_ID $GRP
RUN adduser --disabled-password --gecos "" --uid $USER_ID --gid $GROUP_ID $GRP
WORKDIR $APP_DIR
# RUN chown $USR:$GRP $APP_DIR
ENV USR_HOME=/home/$USR
COPY --from=builder --chown=$USER_ID:$GROUP_ID /root/.local $USR_HOME/.local

USER $USR
ENV PATH=$USR_HOME/.local/bin:$PATH

# COPY --chown=$USER_ID:$GROUP_ID . .

EXPOSE 5000

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000", "--with-threads"]
