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


FAKE_CONFIG_DIR = 'path/to/config'
FAKE_CONFIG_FILENAME = 'config.json'

@pytest.fixture(params=[
    (FAKE_CONFIG_DIR, FAKE_CONFIG_FILENAME),
])
def config_file_path(request):
    '''
    A parametrized fixture that creates a temporary config file in a temporary
    directory. It yields the absolute path to the file and handles teardown.
    
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


def test_fixture_creates_file(config_file_path: Path):
    """
    tests that the fixture correctly creates dirs and file
    """
    logger.info(f'checking {config_file_path = }')
    try:
        assert config_file_path.exists()
    except:
        # alternatively add -x or --exitfirst in pytest params
        pytest.exit(f'fixture failed to create file: {config_file_path=}')


def test_automatic_config_project_root_is_correct():
    '''
    tests that the key PROJECT_ROOT matches the project root path
    '''
    logger.info(f'{CONFIG = }')
    logger.info(f'{sys.path[:2] = }')
    assert CONFIG['PROJECT_ROOT'] == sys.path[1]


def test_find_project_root_no_prj_name():
    '''
    tests that find_project_root finds the project root path without specifying project name
    '''
    root = find_project_root()
    assert str(root) in sys.path[:2]
    assert root == Path(sys.path[1])


def test_find_project_root_w_prj_name():
    '''
    tests that find_project_root finds the project root path specifying project name
    '''
    root = find_project_root('google-cloud-storage-mock')
    logger.info(f'{root = }')
    assert str(root) in sys.path[:2]
    assert root == Path(sys.path[1])


def test_find_config_not_found_when_no_project_root_path_specified(config_file_path: Path):
    '''
    tests that _find_config does not find the config file when no project root path is specified
    '''
    logger.info(f'{config_file_path = }')
    # passing just the file name, it won't find it
    config = _find_config(config_file_path.name)
    logger.info(f'{config = }')
    assert config == None


def test_find_config_success_when_project_root_path_specified(config_file_path: Path):
    '''
    tests that _find_config finds the config file when no project root path is specified
    '''
    logger.info(f'{config_file_path = }')
    # passing just the file name, it won't find it
    config = _find_config(config_file_path.name, Path.cwd())
    logger.info(f'{config = }')
    assert config == config_file_path
