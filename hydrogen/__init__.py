# hydrogen/__init__.py
import os
from .app import app
from .utils import load_yaml_config, logger, configure_logger

def config_me():
    # Load the main configuration file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(base_dir, '..', 'config')
    main_config_file = 'main.yml'

    main_config = load_yaml_config(os.path.join(config_dir, main_config_file))
    if not main_config:
        raise EnvironmentError("Failed to load main configuration file.")

    # Set environment variables based on the config file, only if they're not already set
    os.environ.setdefault("LOG_LEVEL", main_config["logging"]["level"])
    os.environ.setdefault("LOG_VERBOSE", str(main_config["logging"]["verbose"]).lower())
    os.environ.setdefault("LOG_FILES", str(main_config["logging"]["log_files"]).lower())

    # Platforms
    os.environ.setdefault("ANEDOT_ENABLE", str(main_config["platforms"]["anedot"]["enable"]))
    os.environ.setdefault("WINRED_ENABLE", str(main_config["platforms"]["winred"]["enable"]))
    os.environ.setdefault("ACTBLUE_ENABLE", str(main_config["platforms"]["actblue"]["enable"]))

    # App Stuff
    os.environ.setdefault("HOST", main_config["web"]["app_host"])
    os.environ.setdefault("APP_PORT", str(main_config["web"]["app_port"]))



    # Now that environment variables are set, configure the logger
    configure_logger()

def light_it_up():
    host = os.environ.get("HOST", '0.0.0.0')
    port = int(os.environ.get("APP_PORT", 9090))
    is_development = os.environ.get("ENV") == "development"
    # The env stuff is ALL KINDS OF MESSED UP
    logger.info("🌞 The sun is shining!")
    app.run(host=host, port=port, debug=is_development)
