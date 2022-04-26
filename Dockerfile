FROM python:3.9.5-slim

WORKDIR /usr/local/app/

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U poetry

COPY pyproject.toml poetry.lock poetry.toml .env ./
COPY order_service ./order_service/
COPY static ./static/

RUN poetry install --no-dev -n

EXPOSE 5555

CMD [".venv/bin/python", "-m", "order_service"]
#CMD bash
