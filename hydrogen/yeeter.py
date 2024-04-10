# hydrogen/yeeter.py
from .destinations import DataDestination, CSVDestination, BigQueryDestination
from .utils import load_yaml_config, logger
import os

class DataDispatcher:
    @staticmethod
    def get_enabled_destinations(config):
        destinations = []
        logger.debug("Checking for enabled destinations.")

        # CSV destination
        if config.get('destinations', {}).get('csv', {}).get('enable'):
            csv_filename = config['destinations']['csv']['filename']
            destinations.append(CSVDestination(csv_filename))
            logger.info(f"CSV destination enabled with filename: {csv_filename}")

        # BigQuery destination
        bigquery_config = config.get('destinations', {}).get('bigquery', {})
        if bigquery_config.get('enable'):
            platform_name = bigquery_config.get('platform_name', 'default') # TODO Dynamic setting...
            destinations.append(BigQueryDestination(platform_name))
            logger.info(f"BigQuery destination enabled for platform: {platform_name}")

        if not destinations:
            logger.warning("No data destinations are enabled in configuration.")
        return destinations

    @staticmethod
    def dispatch_data(data):
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
        config = load_yaml_config('main.yml', base_path=config_dir)

        if not config:
            logger.error("Failed to load configuration for dispatching data.")
            return

        destinations = DataDispatcher.get_enabled_destinations(config)
        if destinations:
            logger.info("Dispatching data to enabled destinations...")
            for destination in destinations:
                try:
                    destination.send_data(data)
                    logger.info(f"Data dispatched successfully to {type(destination).__name__}.")
                except Exception as e:
                    logger.error(f"Failed to dispatch data to {type(destination).__name__}: {e}")
        else:
            logger.warning("No destinations to dispatch data to.")
