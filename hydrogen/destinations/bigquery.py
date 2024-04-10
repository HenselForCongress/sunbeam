# hydrogen/destinations/bigquery.py
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from .base_destination import DataDestination
from ..utils import logger
import os
import yaml

class BigQueryDestination(DataDestination):
    def __init__(self, platform):
        project_id = os.getenv('GOOGLE_PROJECT_ID')
        self.client = bigquery.Client(project=project_id)
        self.platform = platform
        self.dataset_id = f"{project_id}.{platform}"
        self.table_id = f"{self.dataset_id}.donations" # TODO MOre tables

        self.ensure_dataset_exists()
        self.ensure_table_exists()

    def load_schema_from_config(self, schema_file="config/schemas/donations.yml"): # TODO MOre tables
        try:
            with open(schema_file, "r") as file:
                schema_config = yaml.safe_load(file)
            return [bigquery.SchemaField(name=field['name'],
                                         field_type=field['type'],
                                         mode=field['mode'],
                                         description=field['description']) for field in schema_config]
        except Exception as e:
            logger.error(f"Error loading schema configuration: {e}")
            return []

    def ensure_dataset_exists(self):
        dataset_ref = self.client.dataset(self.platform)
        try:
            self.client.get_dataset(dataset_ref)
            logger.info(f"Dataset '{self.platform}' exists.")
        except NotFound:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            self.client.create_dataset(dataset)
            logger.info(f"Dataset '{self.platform}' created.")

    def ensure_table_exists(self):
        table_ref = self.client.dataset(self.platform).table("donations")
        try:
            self.client.get_table(table_ref)
            logger.info(f"Table 'donations' exists in dataset '{self.platform}'.")
        except NotFound:
            table = bigquery.Table(table_ref)
            table.schema = self.load_schema_from_config()  # Dynamically load schema
            if table.schema:
                self.client.create_table(table)
                logger.info(f"Table 'donations' created in dataset '{self.platform}'.")
            else:
                logger.error("Failed to create table due to schema load error.")

    def send_data(self, data):
        rows_to_insert = [data]
        logger.debug(f'BigQuery Data to insert: \n{rows_to_insert}')
        try:
            errors = self.client.insert_rows_json(self.table_id, rows_to_insert)
            if errors == []:
                logger.info(f"Data successfully written to BigQuery table 'donations' in dataset '{self.platform}'.")
            else:
                logger.error(f"Errors occurred while inserting rows: {errors}")
        except Exception as e:
            logger.error(f"Failed to write data to BigQuery: {e}, Table ID: {self.table_id}")
