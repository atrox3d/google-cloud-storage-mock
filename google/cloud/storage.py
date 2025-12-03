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

logger = logging.getLogger(__name__)

################################################################
# creates fake buckets root path
################################################################
DEBUG = False
FAKE_BUCKETS_ROOT_DIR = CONFIG['FAKE_BUCKETS_ROOT_DIR']
PROJECT_DIRNAME = CONFIG['PROJECT_DIRNAME']
LOG_PREFIX = CONFIG['LOG_PREFIX']
FAKE_BUCKETS_ROOT = str(PROJECT_ROOT / FAKE_BUCKETS_ROOT_DIR)
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


class Blob:
    # @logged(prefix=LOG_PREFIX)    # dont decorate init, infinite recursion
    def __init__(
            self, 
            name, 
            bucket,
        ):
        self.bucket = bucket
        self.name = name
        self.content_type = None
        self.path = self.bucket.path / name
        self.generation = True
        logger.debug(f'Blob.path = {self.path}')
    
    @logged(prefix=LOG_PREFIX)
    def download_as_string(self, encoding: str | None = None):
        '''
        Downloads blob content.
        If encoding is provided, returns a string decoded with that encoding.
        Otherwise, returns raw bytes.
        '''
        with open(self.path, 'rb') as f:
            content_bytes = f.read()
        if encoding:
            return content_bytes.decode(encoding)
        return content_bytes
    
    @property
    def size(self):
        return self.path.stat().st_size

    @logged(prefix=LOG_PREFIX)
    def delete(self, if_generation_match=0):
        ''' deletes blob '''
        if self.path.is_file():
            self.path.unlink()
            logger.info(f"Deleted Blob: {self.path}")
            # Check if the parent directory is now empty and remove it.
            try:
                if not any(self.path.parent.iterdir()):
                    logger.info(f"Removing empty parent directory: {self.path.parent}")
                    self.path.parent.rmdir()
            except FileNotFoundError:
                # This can happen in race conditions or if the parent was already gone.
                logger.warning(f'parent directory not found: {self.path.parent}')
                pass

    @logged(prefix=LOG_PREFIX)
    def exists(self, storage_client):
        ''' checks if blob exists'''
        logger.debug(f'Blob.path = {self.path}')
        exists = self.path.exists()
        return exists
    
    @logged(prefix=LOG_PREFIX)
    def compose(self, sources, if_generation_match=0):
        ''' glues parts into whole file'''
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'wb') as f:
            for source in sources:
                with open(source.path, 'rb') as g:
                    f.write(g.read())
        return

    @logged(prefix=LOG_PREFIX)
    def reload(self):
        ''' useless in local fs '''
        pass

    def __str__(self):      # do not decorate, infinite recursion
        return self.bucket.name + '/' + self.name
    
    def __repr__(self):     # do not decorate, infinite recursion
        # return str(self)
        return f'{self.__class__.__name__}(bucket={self.bucket}, name={self.name}, path={self.path})'


class Bucket:
    @logged(prefix=LOG_PREFIX)
    def __init__(self, name):
        self.name = name
        self.path = Path(FAKE_BUCKETS_ROOT) / name
        logger.info(f'Bucket.path = {self.path}')
    
    @logged(prefix=LOG_PREFIX)
    def blob(self, name) -> Blob:
        return Blob(name, self)
    
    @logged(prefix=LOG_PREFIX)
    def get_blob(self, name) -> Blob:
        ''' short circuito to self.blob for simplicity'''
        return self.blob(name)
    
    @logged(prefix=LOG_PREFIX)
    def copy_blob(self, source_blob:Blob, dest_bucket:'Bucket', dest_path:str, if_generation_match=0):
        logger.debug(f'{dest_bucket = }')
        logger.debug(f'{source_blob = }')
        logger.debug(f'{dest_path = }')
        logger.debug(f'{if_generation_match = }')
        source_path:Path = source_blob.path
        dest_path:Path = dest_bucket.blob(dest_path).path
        logger.debug(f'{source_path = }')
        logger.debug(f'{dest_path = }')
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, dest_path)
        logger.info(f"Successfully copied {source_path} to {dest_path}")    
    
    @logged(prefix=LOG_PREFIX)

    def __str__(self):      # do not decorate, infinite recursion
        return self.name
    
    def __repr__(self):     # do not decorate, infinite recursion
        # return str(self)
        return f'{self.__class__.__name__}(name={self.name}, path={self.path})'
