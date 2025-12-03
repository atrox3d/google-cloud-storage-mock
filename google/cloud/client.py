import logging

from .config import CONFIG
from util import logged
from .bucket import Bucket
from .blob import Blob

logger = logging.getLogger(__name__)
LOG_PREFIX = CONFIG['LOG_PREFIX']

class Client:
    # @logged(prefix=LOG_PREFIX)
    def bucket(self, bucket_name) -> Bucket:
        return Bucket(bucket_name)
    
    # @logged(prefix=LOG_PREFIX)
    def list_blobs(self, bucket_name, prefix, fields) -> list[Blob]:
        ''' lists all blobs in a bucket path '''
        bucket = self.bucket(bucket_name)
        path = bucket.path / prefix
        logger.debug(f'path = {path}')
        files = list(path.glob('**/*'))
        logger.debug(f'files = {files}')
        blobs = [Blob(str(file.relative_to(bucket.path)), bucket) for file in files]   # return glob->Blob
        return blobs
