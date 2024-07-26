from pathlib import Path

from loguru import logger
from sqlalchemy import create_engine, select, text

from pipelines.settings import Settings

settings = Settings()


def is_data_present(date: str) -> bool:
    """Check if the current month data is already present in the database."""
    engine = create_engine(settings.DB_CONNECTION_STRING.get_secret_value())

    query = select(text(f"* FROM {settings.DB_NAME}")).where(text(f"date = '{date}'"))

    with engine.connect() as con:
        result = con.execute(query)

    return result.fetchone() is not None


def import_csv(directory: Path) -> None:
    """Import the CSV files to the database."""
    engine = create_engine(settings.DB_CONNECTION_STRING.get_secret_value())

    files = directory.glob("*.csv")

    if not any(files):
        return

    for file in files:
        logger.info(f"Importing data from {file.name}")

        query = text(
            f"COPY {settings.DB_NAME} FROM '/output/{file.name}' CSV HEADER",
        )

        with engine.connect() as con, con.begin():
            con.execute(query)

        file.unlink()

        logger.success(f"Data from {file.name} imported successfully")
