FROM python:3.10

# copy workspace
WORKDIR workspace
COPY . .

# update environmemnt and install requirements
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# replace openssl file here to get more hash algorithms
RUN rm /usr/lib/ssl/openssl.cnf
RUN cp openssl.cnf /usr/lib/openssl.cnf

# create db tables
RUN python manage.py makemigrations address_api
RUN python manage.py migrate

EXPOSE 8000

