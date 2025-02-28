import logging
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s[%(levelname)s] [%(asctime)s] %(message)s",
    datefmt='%d/%m/%Y %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))

logging.basicConfig(level=logging.INFO, handlers=[handler])

class LogServiceMixin:

    def error_log(self, message: str) -> None:
        logging.error(message)

    def warning_log(self, message: str) -> None:
        logging.warning(message)
    
    def info_log(self, message: str) -> None:
        logging.info(message)
