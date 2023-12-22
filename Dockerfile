FROM python:3.11-alpine3.17 AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-alpine3.17

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories; echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories; apk update && apk add chromium chromium-chromedriver git && pip install --no-cache-dir --upgrade -r /code/requirements.txt 

COPY ./app ./app

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
