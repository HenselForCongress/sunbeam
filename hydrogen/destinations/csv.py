# hydrogen/destinations/csv.py
import csv
from .base_destination import DataDestination
from ..utils import logger

class CSVDestination(DataDestination):
    def __init__(self, filename):
        self.filename = filename

    def send_data(self, data):
        try:
            with open(self.filename, mode='a', newline='') as csv_file:
                fieldnames = data.keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                if csv_file.tell() == 0:  # File is empty, write headers
                    writer.writeheader()
                writer.writerow(data)

            logger.info(f"Data successfully written to {self.filename}")  # Confirmation log

        except Exception as e:
            logger.error(f"Failed to write data to {self.filename}: {e}")
