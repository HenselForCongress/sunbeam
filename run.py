# run.py
import os

def main():
    from hydrogen import config_me, light_it_up,logger


    config_me()  # Set environment variables based on main.yml
    logger.info("🚀 Starting Donation Reporter")

    try:
        # Run hydrops
        logger.info('😃 Starting the sun...')
        light_it_up()
    except Exception as e:
        logger.error("💥 An unexpected error occurred with the hydrogen: %s", str(e), exc_info=True)

if __name__ == "__main__":
    main()
