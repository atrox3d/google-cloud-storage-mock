from pathlib import Path
import shutil
import logging
from util import printstamp, logged
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
FAKE_BUCKETS_ROOT_DIR = CONFIG['FAKE_BUCKETS_ROOT_DIR']
PROJECT_DIRNAME = CONFIG['PROJECT_DIRNAME']
LOG_PREFIX = CONFIG['LOG_PREFIX']
FAKE_BUCKETS_ROOT = str(PROJECT_ROOT / FAKE_BUCKETS_ROOT_DIR)
################################################################
logger.info(f'{FAKE_BUCKETS_ROOT = }')
logger.info(f'{PROJECT_DIRNAME = }')


DEBUG = False

def fgcdebug(message: str) -> None:
    DEBUG and fgclog(message, f'{LOG_PREFIX} DEBUG | ')


def fgclog(message: str, prefix:str=LOG_PREFIX) -> None:
    printstamp(f'{prefix} {message}')


def mock_path(path:Path|str) -> str:
    path = str(path) if isinstance(path, Path) else path
    if path.startswith('gs:/'):
        path = path.replace("gs:/", FAKE_BUCKETS_ROOT)
        return path
    else:
        raise ValueError(f'path must start with "gs:/" : {path = }')


def mock_paths(*path_dicts):
    """
    Iterates through dictionaries and modifies their string values in-place,
    replacing 'gs:/' with the local FAKE_BUCKETS_ROOT.
    This function has side effects.
    """

    result = []
    fgclog("Mocking GCS paths in-place...")
    for d in path_dicts:
        if isinstance(d, dict):
            for key, value in d.items():
                if isinstance(value, str):
                    # d[key] = value.replace("gs:/", FAKE_BUCKETS_ROOT)
                    d[key] = mock_path(value)

        elif isinstance(d, str):
            d = d.replace("gs:/", FAKE_BUCKETS_ROOT)
        result.append(d)
    
    return result


class Client:
    # @logged(prefix=LOG_PREFIX)
    def bucket(self, bucket_name) -> 'Bucket':
        return Bucket(bucket_name)
    
    @logged(prefix=LOG_PREFIX)
    def list_blobs(self, bucket_name, prefix, fields):
        ''' lists all blobs in a bucket path '''
        bucket = self.bucket(bucket_name)
        path = bucket.path / prefix
        fgcdebug(f'path = {path}')
        files = list(path.glob('**/*'))
        fgcdebug(f'files = {files}')
        blobs = [Blob(str(file.relative_to(bucket.path)), bucket) for file in files]   # return glob->Blob
        return blobs


class Blob:
    # @logged(prefix=LOG_PREFIX)
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
        fgcdebug(f'Blob.path = {self.path}')
    
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
            fgclog(f"Deleted Blob: {self.path}")
            # Check if the parent directory is now empty and remove it.
            try:
                if not any(self.path.parent.iterdir()):
                    fgclog(f"Removing empty parent directory: {self.path.parent}")
                    self.path.parent.rmdir()
            except FileNotFoundError:
                # This can happen in race conditions or if the parent was already gone.
                fgclog(f'WARNING | parent directory not found: {self.path.parent}')
                pass

    @logged(prefix=LOG_PREFIX)
    def exists(self, storage_client):
        ''' checks if blob exists'''
        fgcdebug(f'Blob.path = {self.path}')
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
        fgcdebug(f'Bucket.path = {self.path}')
    
    @logged(prefix=LOG_PREFIX)
    def blob(self, name) -> Blob:
        return Blob(name, self)
    
    @logged(prefix=LOG_PREFIX)
    def get_blob(self, name) -> Blob:
        ''' short circuito to self.blob for simplicity'''
        return self.blob(name)
    
    @logged(prefix=LOG_PREFIX)
    def copy_blob(self, source_blob:Blob, dest_bucket:'Bucket', dest_path:str, if_generation_match=0):
        fgcdebug(f'{dest_bucket = }')
        fgcdebug(f'{source_blob = }')
        fgcdebug(f'{dest_path = }')
        fgcdebug(f'{if_generation_match = }')
        source_path:Path = source_blob.path
        dest_path:Path = dest_bucket.blob(dest_path).path
        fgcdebug(f'{source_path = }')
        fgcdebug(f'{dest_path = }')
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, dest_path)
        fgclog(f"Successfully copied {source_path} to {dest_path}")    
    
    @logged(prefix=LOG_PREFIX)

    def __str__(self):      # do not decorate, infinite recursion
        return self.name
    
    def __repr__(self):     # do not decorate, infinite recursion
        # return str(self)
        return f'{self.__class__.__name__}(name={self.name}, path={self.path})'
