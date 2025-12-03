import logging
from pathlib import Path
import shutil

from .config import CONFIG
from util import logged
from .blob import Blob

logger = logging.getLogger(__name__)
LOG_PREFIX = CONFIG['LOG_PREFIX']
FAKE_BUCKETS_ROOT = CONFIG['FAKE_BUCKETS_ROOT']


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
