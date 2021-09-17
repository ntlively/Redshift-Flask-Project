FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt /code/

# Installing client libraries and any other package you need
RUN apk update && apk add libpq

# Installing build dependencies
# For python3 you need to add python3-dev
RUN apk update
RUN apk add --virtual .build-deps gcc musl-dev postgresql-dev g++ zlib-dev make jpeg-dev libjpeg python3 python3-dev gfortran
RUN apk --no-cache add musl-dev linux-headers g++ zlib gcc musl-dev postgresql-dev g++ zlib-dev make jpeg-dev libjpeg python3 python3-dev gfortran

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps
# Installing and build python module
RUN pip install psycopg2
RUN pip install python-decouple

# Delete build dependencies
RUN apk del .build-deps
RUN pip install --upgrade setuptools wheel
RUN pip install --upgrade pip
RUN pip install ez_setup

RUN pip install pybind11
RUN pip install numpy
RUN pip install pandas
RUN pip install Pillow
RUN pip install matplotlib
RUN pip install mpld3

RUN pip install -r requirements.txt --no-cache-dir
COPY . /code/
ENV FLASK_APP hello.py
CMD flask run --host=0.0.0.0
 