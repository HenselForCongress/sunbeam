# hydrogen/utils/config_loader.py
import os
import yaml
from .logging import logger


def load_yaml_config(file_path, base_path=None):

    if base_path:
        file_path = os.path.join(base_path, file_path)
    logger.debug("📄 Loading YAML conf from: %s", file_path)
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.debug(f'YAML Config:\n %s', config)
        logger.debug("✅ YAML config loaded successfully.")
        return config
    except FileNotFoundError:
        logger.error("🚨 YAML file not found at path: %s", file_path)
        return None
    except yaml.YAMLError as e:
        logger.error("🚨 Error parsing YAML file: %s", str(e))
        return None
    except Exception as e:
        logger.error("🚨 An undefined error occurred while loading YAML configuration: %s", str(e))
        return None
