FROM python:3.9.5

WORKDIR /usr/local/app/

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U poetry

COPY pyproject.toml poetry.lock poetry.toml alembic.ini .env config.py db.py logger_config.py ./
COPY alembic ./alembic/
COPY models ./models/
COPY order_service ./order_service/
COPY static ./static/

RUN poetry install --no-dev -n

EXPOSE 8000

CMD [".venv/bin/python", "-m", "order_service"]
#CMD bash
