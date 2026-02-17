from loguru import logger
import sys

def setup_logger():
    logger.remove()

    logger.add(
        sys.stdout, 
        format="<blue>{time:YYYY:MM:DD} {time:HH:mm:ss:SSS}</blue> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        colorize=True
    )

