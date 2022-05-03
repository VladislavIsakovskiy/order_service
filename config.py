from os import environ, path

from dotenv import load_dotenv


# Find .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

# db
ALEMBIC_DATABASE_DRIVER = environ.get("ALEMBIC_POSTGRES_DRIVER", "postgresql")
DATABASE_DRIVER = environ.get("POSTGRES_DRIVER", "postgresql+asyncpg")
DATABASE_HOST = environ.get("POSTGRES_HOST", "localhost")
DATABASE_PORT = environ.get("POSTGRES_PORT", "5432")
DATABASE_NAME = environ.get("POSTGRES_DB", "order_service")
DATABASE_USER = environ.get("POSTGRES_USER", "postgres")
DATABASE_PASSWORD = environ.get("POSTGRES_PASSWORD", "postgres")
DATABASE_URL = (
    f"{DATABASE_DRIVER}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)
