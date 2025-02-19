#
FROM python:3.10 as requirements-stage

#
WORKDIR /tmp

#
RUN pip install poetry

#
COPY ./pyproject.toml ./poetry.lock* /tmp/

#
RUN poetry export --only main --without-hashes --without-urls | awk '{ print $1 }' FS=';' > requirements.txt

#
FROM python:3.10

#
WORKDIR /

#
COPY --from=requirements-stage /tmp/requirements.txt /requirements.txt

#
RUN pip install -U -r /requirements.txt

#
COPY . /

#
CMD ["fastapi", "run", "main.py", "--port", "8000"]
