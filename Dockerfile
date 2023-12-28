FROM python:3.11.7


RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir -U pdm


COPY pyproject.toml pdm.lock /

# RUN pdm sync --prod --no-editable

RUN /bin/sh -c set -ex; \
    pdm export --prod --without-hashes -f requirements -o requirements.txt; \
    pip install -U -r requirements.txt


COPY config.py manage.py /
COPY data /data
COPY petroleum_prices /petroleum_prices
COPY prices_analyzer /prices_analyzer
COPY rail_tariff /rail_tariff
COPY spimex_parser /spimex_parser
COPY users /users
COPY templates /templates


CMD ["manage.py", "runserver", "0.0.0.0:8000"]
