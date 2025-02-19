FROM python:3.10

#
WORKDIR /

#
COPY . /

#
RUN pip install -U -r /requirements.txt

#
CMD ["fastapi", "run", "main.py", "--port", "8000"]
