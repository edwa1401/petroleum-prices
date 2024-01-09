# petroleum-prices


## Install locally:
### Clone repo: 
```git clone https://github.com/edwa1401/petroleum-prices.git```


### Create file **_.env_** with variables:
_SECRET_KEY=django_secret_key_
_POSTGRES_DB=postgres_db_
_POSTGRES_USER= postgres_user_
_POSTGRES_PASSWORD=postgres_password_
_POSTGRES_HOST='127.0.0.1'_
_REDIS_LOCATION_CASH_URL='redis://127.0.0.1:6379/1'_
_CELERY_BROKER_URL='redis://127.0.0.1:6379/0'_
_ALLOWED_HOSTS='localhost,127.0.0.0.1'_

### Install and run **docker decktop**: https://docs.docker.com/desktop/

### Build docker containers:  

```docker compose pull```
```docker compose build```
```docker compose up-d postgresdb```
```docker compose up-d redis```
```docker compose up-d nginx```
```docker compose up-d worker```
```docker compose up-d web```

### Follow link
``` http://127.0.0.0.1```


## Deploy

### Rent virtual maschine with static IP / rent host name
Input to server via ssh
run commands ```sudo apt-get
sudo apt-get dist-upgrade -y
sudo apt-get autoremote -y
sudo reboot```

_optionally (for rented host name) - add public ip to rented host in host settings_

### From local publish docker container
At '''https://github.com/edwa1401/petroleum-prices.git''' run *** publish docker container ***
in **github action** section

### Pull docker image ```docker pull <imagename>``` _for mac add_ ```--platform=linux/amd64```
 _imagename: <ghcr.io/edwa1401/petroleum-prices:main>_

### Create docker compose for deploy _deploy/docker-compose.yaml_
change commands **build: .** by **image: <imagename>** for **web** and **worker** containers

_for Mac run_ ```export DOCKER_DEFAULT_PLATFORM=linux/amd64```

### Create .env for deploy
copy dev _.env_
change variables
```POSTGRES_HOST=postgresdb```
```CELERY_BROKER_URL=redis://redis:6379/0```

### Input to server via ssh

### Install docker https://docs.docker.com/engine/install/ubuntu/#uninstall-old-versions
_include postinstall steps_

###  Copy files to server

Copy files _deploy/docker-compose.yaml_  and _deploy/.env_

in **.env**  add public ip/host name for variables:
**_ALLOWED_HOSTS_**
**CSRF_TRUSTED_ORIGINS**
**CSRF_ALLOWED_ORIGINS**
**CORS_ORIGINS_WHITELIST** _Cross-Origin Resource Sharing for DRF_

create dir _nginx_, folders _nginx/ssl_ and _nginx/conf.d_

copy file **nginx.conf** to _nginx/conf.d_

### Bundle SSL certificates
create/copy recieved ssl certificates in folder _nginx/ssl_ as:
**_domain.crt_**
**_intermediate.crt_**
**_caroot.crt_**

**_domain.key_** _private key_
**_request.csr_** _request for cert_

run
```cd /etc/nginx/ssl```
```cat domain.crt intermediate.crt caroot.crt > domain.ca-bundle```

check _hash amounts_ for cert, private key and request:
run
```openssl x509 -noout -modulus -in domain.crt | openssl md5```
```openssl x509 -noout -modulus -in domain.ca-bundle | openssl md5```
```openssl rsa -noout -modulus -in private.key | openssl md5```
```openssl req -noout -modulus -in request.csr | openssl md5```
_(stdin)= hash amount_

### Create docker container
run
```docker compose pull```
```docker compose up-d postgresdb```
```docker compose up-d redis```
```docker compose up-d nginx```
```docker compose up-d worker```

### Follow link
``` https:\\project's_host_name```
