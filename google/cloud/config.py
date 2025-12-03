import json
from pathlib import Path
import logging
import sys

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "FAKE_BUCKETS_ROOT_DIR": "_FAKE_BUCKET/",
    "PROJECT_DIRNAME": sys.path[0],
    "LOG_PREFIX": "FAKE_GOOGLE_CLOUD | "
}


def _find_config(
    config_json_filename:str,
    project_root_path:Path=None
) -> Path | None:
    '''
    tries to load the specified json file
    - if a project root path is specified tries in all project
    - if not, tries simply in the current pwd
    
    :param config_json_filename: Description
    :type config_json_filename: str
    :param project_root_path: Description
    :type project_root_path: Path
    :return: Description
    :rtype: Path | None
    '''
    config_json = None
    
    if project_root_path:
        logger.info(f'searching {config_json_filename} in {project_root_path}...')
        try:
            config_json = next(project_root_path.glob(config_json_filename))
            logger.info(f'found {config_json}')
        except StopIteration:
            logger.info(f'{config_json_filename} not found, creating default config')
    elif Path(config_json_filename).exists():
        # try directly in current pwd
        logger.info(f'no project root available, using path {config_json}...')
        config_json = Path(config_json_filename)
    else:
        config_json = None
    return config_json


def get_config(
    config_json_filename:str = 'gcs.json',
    project_root_path:Path=None
) -> dict[str, str]:
    '''
    loads config from json file if it exists, otherwise creates default config

    :param config_json_filename: the filename of the config json file
    :type config_json_filename: str
    :param project_root_path: the project root path
    :type project_root_path: Path
    :return: a config dictionary
    :rtype: dict[str, str]
    '''

    config_json = _find_config(config_json_filename, project_root_path)
    if config_json:
        logger.info(f'loading config from {config_json}...')
        with open(config_json) as fp:
            config = json.load(fp)
    else:
        logger.info(f'{config_json} not found, creating default config')
        config = DEFAULT_CONFIG
    logger.info(f'{config = }')
    return config


def find_project_root(project_dir_name:str=None) -> Path:
    '''
    tries to find the path of the project root directory
    if project_dir_name is None assumes the first entry in sys.path
    
    :param project_dir_name: name of the project root directory
    :type project_dir_name: str
    :return: the path of the project root directory
    :rtype: Path
    :raises FileNotFoundError: if the project root directory cannot be found
    '''
    if project_dir_name:
        pwd = Path.cwd()
        while pwd.name != project_dir_name:
            pwd = pwd.parent
            if pwd == Path('/').resolve():
                # we reached the root of the fs without finding it
                raise FileNotFoundError(f'cannot find {project_dir_name}')
        project_root_path = pwd
    else:
        project_root_path = Path(sys.path[0])
    return project_root_path


PROJECT_ROOT = find_project_root()
CONFIG = get_config(project_root_path=PROJECT_ROOT)
CONFIG['PROJECT_DIRNAME'] = CONFIG.get('PROJECT_DIRNAME') or PROJECT_ROOT.name
CONFIG['FAKE_BUCKETS_ROOT'] = str(PROJECT_ROOT / CONFIG['FAKE_BUCKETS_ROOT_DIR'])
logger.info(f'{CONFIG = }')
