# Zeply Crypto REST API

This Github repo is for a REST API built with Django, that generates and stores cryptocurrency addresses for Bitcoin (BTC) and Ethereum (ETH).
The project requirements include implementing various endpoints using the Django REST Framework, associating each address with an integer ID, and securely storing private keys. 
There is also a section for improvements that could be made to the project, such as adding SSL for a more secure connection and implementing authentication for the API.

##  Project Requirements 
- REST API (Met)
    - POST: Generate Address 
    - GET: List Address 
    - GET: Retrieve Address 
- Support for BTC and ETH (Met)
- Associate each address in the database with integer id (Met)
- Generate multiple addresses using a single private key (TODO)
- Store sensitive data securely (Private keys are encrypted)
- Wallet database recovery (TODO)
- Should include tests (Includes automated tests)
- Documentation for manual testing (Met)
- Git repo (Met)

## Prerequisites
- Docker
- Docker Compose
- Curl

## Build Instructions
In the main project directory run:
```commandline
docker-compose up -d
```
This should build the container and run the application on port 8000. 
## Manual Testing Commands

To generate new address and store it in the database. Replace BTC with ETH for generating an Ethereum address. 
```commandline
curl -X POST http://localhost:8000/Crypto_Address_Table/generate_address/ -H "Content-Type: application/json" -d '{"currency": "BTC"}'
```
List all addresses in the table.
```commandline
curl -X GET http://localhost:8000/Crypto_Address_Table/
```
Get the 1st row of the table. Replace 1 with whatever index you would like to fetch. 
```commandline
curl -X GET http://localhost:8000/Crypto_Address_Table/1/
```
You can also put: 
```html
http://localhost:8000/
```
... in the browser to view the application from your browser. 
## Tests
In /address_api/tset.py contains tests for each of the requests. 
You can run them with:
```commandline
python manage.py test
```
However, you would need to stop the process in the docker container to use this. 

# Improvements

- Include Postgresql with SSL for more secure connection
- Include authentication on the REST api 
- Database regular backup
- Validate encryption algorithms and libraries are safe