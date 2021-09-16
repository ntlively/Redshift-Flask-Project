FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt /code/

# Installing client libraries and any other package you need
RUN apk update && apk add libpq

# Installing build dependencies
# For python3 you need to add python3-dev
RUN apk add --virtual .build-deps gcc musl-dev postgresql-dev

# Installing and build python module
RUN pip install psycopg2
RUN pip install python-decouple

# Delete build dependencies
RUN apk del .build-deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code/
ENV FLASK_APP hello.py
CMD flask run --host=0.0.0.0
 