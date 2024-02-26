# Petroleum-prices project


## For developers:

### Install locally:

* Clone repo:
```git clone https://github.com/edwa1401/petroleum-prices.git```

* Create file **_.env_** with variables:
```env
SECRET_KEY=<django_secret_key>
POSTGRES_DB=<postgres_db>
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
POSTGRES_HOST=<127.0.0.1>
REDIS_LOCATION_CASH_URL=<redis://127.0.0.1:6379/1>
CELERY_BROKER_URL=<redis://127.0.0.1:6379/0>
ALLOWED_HOSTS=<localhost,127.0.0.0.1>
TAG=<0.0.6>
DJANGO_SETTINGS_MODULE=<petroleum_prices.settings>
DEBUG=<True>
```

* Install and run <a href="https://docs.docker.com/desktop/" class="external-link" target="_blank"><strong>Docker decktop</strong></a>

* Build docker containers:
``` run commands
docker compose pull
docker compose build
docker compose up-d postgresdb
docker compose up-d redis
docker compose up-d nginx
docker compose up-d worker
docker compose up-d web
```

* Follow link <a href="http://127.0.0.0.1" class="external-link" target="_blank"><strong>http://127.0.0.0.1</strong></a>


### Deploy, CI/CD

* Rent virtual maschine with static IP / rent host name

* Create ssh

* Input to server via ssh

* Run commands:
```
sudo apt-get
sudo apt-get dist-upgrade -y
sudo apt-get autoremote -y
sudo reboot
```
* _Optionally (for rented host name) - add public ip to rented host in host settings_

* Install docker (follow <a href="https://docs.docker.com/engine/install/ubuntu/#uninstall-old-versions" class="external-link" target="_blank"><strong>instructions</strong></a> _include postinstall steps_)

* Create **.env** file:
    * create variables from section **Install locally/Create file **_.env_** with variables:**
    * add public ip/host name for variables:
```env
ALLOWED_HOSTS=<www.petroleum-prices.ru,petroleum-prices.ru>
CSRF_TRUSTED_ORIGINS=<https://petroleum-prices.ru,https://www.petroleum-prices.ru>
CSRF_ALLOWED_ORIGINS=<https://petroleum-prices.ru,https://www.petroleum-prices.ru>
CORS_ORIGINS_WHITELIST=<https://petroleum-prices.ru,https://www.petroleum-prices.ru>
DEBUG=False
```

* Create folders for nginx conf:
run
```
mkdir nginx
mkdir nginx/ssl
mkdir nginx/conf.d
```

* Copy file **deploy/nginx/conf.d/nginx.conf** to folder _nginx/conf.d_

* Bundle SSL certificates
    * create/copy recieved ssl certificates in folder **_nginx/ssl_** as:
        **_domain.crt_**
        **_intermediate.crt_**
        **_caroot.crt_**

        **_domain.key_** _private key_
        **_request.csr_** _request for cert_

    * bundle certs
    run
    ```
    cd /etc/nginx/ssl
    cat domain.crt intermediate.crt caroot.crt > domain.ca-bundle`
    ```
    * check **_hash amounts_** for cert, private key and request:
    run
    ```
    openssl x509 -noout -modulus -in domain.crt | openssl md5
    openssl x509 -noout -modulus -in domain.ca-bundle | openssl md5
    openssl rsa -noout -modulus -in private.key | openssl md5
    openssl req -noout -modulus -in request.csr | openssl md5
    ```
    _(stdin)= hash amount_

* Create docker container:
run
```
docker compose pull
docker compose up-d postgresdb
docker compose up-d redis
docker compose up-d nginx
docker compose up-d worker
docker compose up-d web
```

* Check link <a href="https://www.petroleum-prices.ru" class="external-link" target="_blank"><strong>petroleum-prices.ru</strong></a>
