from pathlib import Path
import shutil
import logging
from util import logged
from .config import (
    get_config, 
    find_project_root,
    CONFIG, 
    PROJECT_ROOT
)

from .client import Client
from .bucket import Bucket
from .blob import Blob

logger = logging.getLogger(__name__)

################################################################
# creates fake buckets root path
################################################################
DEBUG = False
FAKE_BUCKETS_ROOT_DIR = CONFIG['FAKE_BUCKETS_ROOT_DIR']
PROJECT_DIRNAME = CONFIG['PROJECT_DIRNAME']
LOG_PREFIX = CONFIG['LOG_PREFIX']
FAKE_BUCKETS_ROOT = CONFIG['FAKE_BUCKETS_ROOT']
################################################################
logger.info(f'{FAKE_BUCKETS_ROOT = }')
logger.info(f'{PROJECT_DIRNAME = }')


def mock_path(path:Path|str, buckets_root:str=FAKE_BUCKETS_ROOT) -> str:
    '''
    translates a gs:// path to a local path
    
    :param path: the gs:// path to translate
    :type path: Path | str
    :param buckets_root: the local folder parent of the fake buckets
    :type buckets_root: str
    :return: new translated local path
    :rtype: str
    '''
    path = str(path) if isinstance(path, Path) else path
    if path.startswith('gs:/'):
        path = path.replace("gs:/", buckets_root)
        return path
    else:
        raise ValueError(f'path must start with "gs:/" : {path = }')


def mock_paths(*path_dicts_or_strings:dict|str, buckets_root:str=FAKE_BUCKETS_ROOT) -> list[dict | str]:
    '''
    for each dict or string in path_dicts_or_strings
    mocks whatever value in the dicts that is a string beginning with gs:// with a local path
    or whatever value in the strings
    
    :param path_dicts_or_strings: a variable list of dicts separated with commas (like *args)
    :type path_dicts_or_strings: dict|str
    :return: a list of modified dicts
    :rtype: list[dict | str]
    '''

    result = []
    logger.info("Mocking GCS paths in-place...")
    for item in path_dicts_or_strings:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, str):
                    # d[key] = value.replace("gs:/", FAKE_BUCKETS_ROOT)
                    item[key] = mock_path(value, buckets_root)
                    
        elif isinstance(item, str):
            item = mock_path(item, buckets_root)
        result.append(item)
    
    return result
