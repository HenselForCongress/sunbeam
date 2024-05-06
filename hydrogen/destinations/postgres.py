# hydrogen/destinations/postgres.py
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from .base_destination import DataDestination
from ..utils import logger
import os

class PostgresDestination(DataDestination):
    def __init__(self):
        db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:" \
                 f"{os.getenv('POSTGRES_PASSWORD')}@" \
                 f"{os.getenv('POSTGRES_HOST')}:" \
                 f"{os.getenv('POSTGRES_PORT')}/" \
                 f"{os.getenv('POSTGRES_DATABASE')}"
        self.engine = create_engine(db_url, echo=True, future=True)

    def send_data(self, data):
        # Constructing the SQL statement with named parameters
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f":{key}" for key in data.keys()])
        query = f"INSERT INTO finance.donations ({columns}) VALUES ({placeholders})"
        logger.debug(f"Query: {query}")

        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            session.execute(text(query), data)
            session.commit()  # Explicitly committing the transaction
            logger.info("Data successfully written to PostgreSQL in finance.donations")
        except SQLAlchemyError as e:
            session.rollback()  # Ensure rollback in case of an error
            logger.error(f"Failed to write data to PostgreSQL in finance.donations: {e}")
        finally:
            session.close()  # Ensure the session is closed after operation
