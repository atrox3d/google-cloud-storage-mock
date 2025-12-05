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


def test_automatic_config():
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


@pytest.fixture
def config_json():
    cwd = Path.cwd()
    logger.info(f'{cwd = }')
    config_dir = cwd / '_test_/config'
    config_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f'{config_dir = }')
    config_path = config_dir / 'gcs.json'
    logger.info(f'creating {config_path = }')
    config_path.touch()
    yield config_path
    logger.info(f'removing {config_dir.parent}')
    assert config_dir.parent != cwd
    assert config_dir.parent.is_relative_to(cwd)
    shutil.rmtree(config_dir.parent)


def test_fixture(config_json:Path):
    logger.info(f'checking {config_json = }')
    assert config_json.exists()


