FROM python:3.10

WORKDIR workspace

COPY . .

# update environmemnt and install requirements
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# replace openssl file here to get more hash algorithms
RUN rm /usr/lib/ssl/openssl.cnf
RUN cp openssl.cnf /usr/lib/openssl.cnf
RUN rm -r address_api/migrations

#RUN apt install python3-dev libpq-dev postgresql postgresql-contrib


# create db tables
#RUN rm -r address_api/migrations
RUN python manage.py makemigrations address_api
RUN python manage.py migrate

EXPOSE 8000

