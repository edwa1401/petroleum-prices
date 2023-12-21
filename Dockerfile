FROM python:3.11.7

WORKDIR /app

RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir -U pdm


COPY pyproject.toml pdm.lock /app/

# RUN pdm sync --prod --no-editable

RUN /bin/sh -c set -ex; \
    pdm export --prod --without-hashes -f requirements -o requirements.txt; \
    pip install -U -r requirements.txt


COPY config.py manage.py /app/
COPY data /app/data
COPY petroleum_prices /app/petroleum_prices
COPY prices_analyzer /app/prices_analyzer
COPY rail_tariff /app/rail_tariff
COPY spimex_parser /app/spimex_parser
COPY users /app/users
COPY templates /app/templates


CMD ["manage.py", "runserver", "0.0.0.0:8000"]
