import logging
from pathlib import Path
import sys
import shutil
logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(module)10s | %(funcName)15s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
import pytest
from google.cloud.config import (
    CONFIG, 
    find_project_root, 
    get_config, 
    _find_config
)


logger = logging.getLogger(__name__)


def test_automaitic_config():
    logger.info(f'{CONFIG = }')
    logger.info(f'{sys.path[:2] = }')
    assert CONFIG['PROJECT_ROOT'] == sys.path[1]


def test_find_project_root_no_prj_name():
    root = find_project_root()
    assert root == Path(sys.path[1])


def test_find_project_root_w_prj_name():
    root = find_project_root('google-cloud-storage-mock')
    print(f'{root = }')
    assert root == Path(sys.path[1])

