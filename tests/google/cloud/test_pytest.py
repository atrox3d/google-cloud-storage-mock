import logging
logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(module)10s | %(funcName)15s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

from google.cloud import storage

logger = logging.getLogger(__name__)

def test_1():
    import sys
    print('hello', sys.path)
    logger.warning(sys.path)
