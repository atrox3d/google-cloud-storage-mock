from pathlib import Path
import sys
import shutil
import pytest
import logging
logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(module)10s | %(funcName)15s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

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
def fixture_config_json(request):
    '''
    Fixture, create temp config json file in temp path
    as specified by @pytest.mark.parametrize
    
    :param request: object containing param attribute:
        a tuple of (relative_path, filename)
    :type request: FixtureRequest
    '''
    try:
        CWD = Path.cwd()
        logger.info(f'{CWD = }')
        assert str(CWD) in sys.path[:2]
        logger.info(f'SUCCESS {CWD=} is in the first two import paths')
    except AssertionError:
        logger.critical(f'please check pytest cwd')
        logger.critical(f'{CWD = }')
        logger.critical(f'{sys.path[:2]}')
        raise

    relative_config_path, config_filename = request.param
    relative_config_path = Path(relative_config_path)
    logger.info(f'{relative_config_path = }')
    logger.info(f'{config_filename = }')

    absolute_config_dir:Path = CWD / relative_config_path
    absolute_config_path:Path = absolute_config_dir / config_filename
    logger.info(f'{absolute_config_path = }')
    
    absolute_config_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f'{absolute_config_dir = }')
    logger.info(f'creating {absolute_config_path = }')
    absolute_config_path.touch()
    yield absolute_config_path

    root_of_test_path = CWD / relative_config_path.parts[0]
    logger.info(f'removing {root_of_test_path = }')
    # protect project path
    assert root_of_test_path != CWD
    # ensure path is relative to project path
    assert root_of_test_path.is_relative_to(CWD)
    shutil.rmtree(root_of_test_path)


@pytest.mark.parametrize(
    'fixture_config_json',
    [('path/to/config', 'config.json')],
    indirect=True
)
def test_fixture(fixture_config_json:Path):
    logger.info(f'checking {fixture_config_json = }')
    assert fixture_config_json.exists()


@pytest.mark.parametrize(
    'fixture_config_json',
    [('path/to/config', 'config.json')],
    indirect=True
)
def test_find_config_no_project_root(fixture_config_json):
    logger.info(f'{fixture_config_json = }')
    return
    config = _find_config('gcs.json')
    logger.info(f'{config = }')
    assert config == fixture_config_json