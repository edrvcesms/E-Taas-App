import logging

logger = logging.getLogger("e-taas")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)