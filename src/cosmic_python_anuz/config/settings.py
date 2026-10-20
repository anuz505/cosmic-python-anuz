import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "change_this_password")
    db_name = os.environ.get("DB_NAME", "app_db")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"


engine = create_async_engine(url=get_postgres_uri())

DEFAULT_SESSION_FACTORY  = async_sessionmaker(bind=engine, expire_on_commit=False)
