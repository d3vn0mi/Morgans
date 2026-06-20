import logging 


def setup_logger():
    # Create a logger
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)  # Set the minimum logging level

    # Guard against duplicate handlers: setup_logger() is called from several
    # modules/functions, and re-adding handlers to the same named logger would
    # cause every message to be emitted multiple times.
    if logger.handlers:
        return logger

    # Create a file handler that logs messages to a file
    file_handler = logging.FileHandler('logfile.log')
    file_handler.setLevel(logging.DEBUG)  # Set the minimum logging level for this handler

    # Create a stream handler that logs messages to the console/terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)  # Set the minimum logging level for this handler

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger