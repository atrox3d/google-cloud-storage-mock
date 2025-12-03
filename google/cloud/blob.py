import logging
from .config import CONFIG
from util import logged

logger = logging.getLogger(__name__)
LOG_PREFIX = CONFIG['LOG_PREFIX']
AUTO_CREATE_DIRS = CONFIG['AUTO_CREATE_DIRS']

class Blob:
    # @logged(prefix=LOG_PREFIX)    # dont decorate init, infinite recursion
    def __init__(
            self, 
            name, 
            bucket,
            auto_create_dirs:bool=AUTO_CREATE_DIRS        
    ):
        self.bucket = bucket
        self.name = name
        self.content_type = None
        self.path = self.bucket.path / name
        self.generation = True
        self.auto_create_dirs = auto_create_dirs
        if auto_create_dirs:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f'Blob.path = {self.path}')

    
    # @logged(prefix=LOG_PREFIX)
    def download_as_string(self, encoding: str | None = None) -> str:
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
    def size(self) -> int:
        return self.path.stat().st_size

    # @logged(prefix=LOG_PREFIX)
    def delete(self, if_generation_match=0) -> None:
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

    # @logged(prefix=LOG_PREFIX)
    def exists(self, storage_client) -> bool:
        ''' checks if blob exists'''
        logger.debug(f'Blob.path = {self.path}')
        exists = self.path.exists()
        return exists
    
    # @logged(prefix=LOG_PREFIX)
    def compose(self, sources, if_generation_match=0) -> None:
        ''' glues parts into whole file'''
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'wb') as f:
            for source in sources:
                with open(source.path, 'rb') as g:
                    f.write(g.read())

    # @logged(prefix=LOG_PREFIX)
    def reload(self):
        ''' useless in local fs '''
        pass

    def __str__(self) -> str:      # do not decorate, infinite recursion
        return self.bucket.name + '/' + self.name
    
    def __repr__(self) -> str:     # do not decorate, infinite recursion
        # return str(self)
        return f'{self.__class__.__name__}(bucket={self.bucket}, name={self.name}, path={self.path})'
