import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.StreamHandler(),
                            logging.FileHandler('log_file.log', mode='w')],
                        encoding='utf-8'
                        )
    return logging.getLogger()
