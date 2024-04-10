# hydrogen/app.py
from flask import Flask, request, jsonify
from .utils import logger
from .yeeter import DataDispatcher
import os

app = Flask(__name__)


def map_fields(platform, data):
    # Accessing FIELD_MAPPINGS from app.config
    field_mappings = app.config.get('FIELD_MAPPINGS', {})
    mapped_data = {}

    for dest_field, mappings in field_mappings.items():
        source_field = mappings.get(platform)
        if source_field:
            try:
                keys = source_field.split(".")
                value = data
                found = True
                for key in keys:
                    if key in value:
                        value = value[key]
                    else:
                        found = False
                        break  # Stop trying to access deeper levels if key is not found

                if found:
                    mapped_data[dest_field] = value
                    logger.debug(f"Field '{dest_field}' mapped successfully from source '{source_field}'.")
                else:
                    logger.warning(f"Source field '{source_field}' not found in payload for platform {platform}.")
            except KeyError as e:
                logger.warning(f"Error: Mapping field {source_field} not found for platform {platform}. {e}")
            except Exception as e:
                logger.error(f"Error: Exception while mapping field '{source_field}' to '{dest_field}'. {e}")
        else:
            logger.info(f"No mapping for '{dest_field}' in platform '{platform}'. Skipping.")

    return mapped_data

def create_platform_handler(platform):
    def platform_endpoint():
        data = request.json
        app.logger.info(f"Received data on {platform} endpoint: {data}")

        # Map fields according to the configuration
        mapped_data = map_fields(platform, data)
        app.logger.debug(f"Mapped data for {platform}: {mapped_data}")

        # Dispatch the mapped data to enabled destinations
        DataDispatcher.dispatch_data(mapped_data)
        app.logger.info(f"Dispatched mapped data for {platform} to the configured destinations.")

        return jsonify({"status": "success", "mapped_data": mapped_data}), 200
    return platform_endpoint

def create_endpoints(platforms):
    @app.route('/')
    def home():
        return "Donation Watch Service is running!"

    # Dynamically configure endpoints based on the platforms enabled in the config
    for platform, details in platforms.items():
        if details.get('enable'):
            app.add_url_rule(f'/{platform}', view_func=create_platform_handler(platform), methods=['POST'])

    app.logger.info("Endpoints dynamically configured based on enabled platforms.")

def setup_app():
    # Load platforms configuration
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(base_dir, '..', 'config')
    from .utils import load_yaml_config  # Moved inside to avoid potential import cycles

    platforms_config = load_yaml_config('main.yml', base_path=config_dir)["platforms"]
    fields_config = load_yaml_config('fields.yml', base_path=config_dir)["fields"]
    app.config['FIELD_MAPPINGS'] = {k: {k2: v2 for k2, v2 in v.items() if v2 is not None} for k, v in fields_config.items()}

    create_endpoints(platforms_config)

setup_app()
