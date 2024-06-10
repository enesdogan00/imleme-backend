FROM python:3.11-alpine3.19 AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-alpine3.19

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN  apk update && apk add --no-cache \
chromium \
chromium-chromedriver \
bash \
curl \
jq \
make \
g++ \
openjdk11-jdk \
nodejs \
npm \
git \
zlib-dev && pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt 

ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_PATH=/usr/lib/chromium/

COPY ./app ./app

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
