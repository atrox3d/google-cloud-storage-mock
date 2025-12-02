import json
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


def get_or_load_config(config_json_path:str = 'gcs.json') -> dict[str, str]:
    ################################################################
    # create/load config
    ################################################################
    config_json = Path(config_json_path)
    logger.info(f'trying to load config from {config_json}...')
    if config_json.exists():
        with open(config_json) as fp:
            config = json.load(fp)
    else:
        logger.info(f'{config_json} not found, creating default config')
        config = {
            "FAKE_BUCKETS_ROOT_DIR": "_FAKE_BUCKET/",
            "PROJECT_DIRNAME": "project_root_dir",
            "LOG_PREFIX": "FAKE_GOOGLE_CLOUD | "
        }
    logger.info(f'{config = }')
    return config


def find_project_root(project_dir_name:str) -> Path:
    pwd = Path.cwd()
    while pwd.name != project_dir_name:
        pwd = pwd.parent
        # print(f'pwd = {pwd}')
        if pwd == Path('/').resolve():
            raise FileNotFoundError(f'cannot find {project_dir_name}')
    return pwd

CONFIG = get_or_load_config()
PROJECT_ROOT = find_project_root(CONFIG['PROJECT_DIRNAME'])
