import logging
from pathlib import Path
import shutil
logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(module)10s | %(funcName)15s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

from google.cloud import storage

logger = logging.getLogger(__name__)

def test_sys_path():
    import sys
    logger.info(sys.path)


def test_new_bucket_auto_create_dirs():
    logger.info(f'{storage.FAKE_BUCKETS_ROOT = }')
    BUCKET_DIRNAME = 'test-bucket'

    bucket_path = Path(storage.FAKE_BUCKETS_ROOT) / BUCKET_DIRNAME
    bucket_path.exists() and shutil.rmtree(bucket_path)
    assert bucket_path.exists() == False

    bucket = storage.Bucket(BUCKET_DIRNAME, auto_create_dirs=True)
    logger.info(f'{bucket.path = }')
    assert bucket.path == bucket_path
    assert bucket.path.exists()
    assert bucket.path.is_dir()
    bucket_path.rmdir()


def test_new_bucket_dont_create_dirs():
    logger.info(f'{storage.FAKE_BUCKETS_ROOT = }')
    BUCKET_DIRNAME = 'test-bucket'

    bucket_path = Path(storage.FAKE_BUCKETS_ROOT) / BUCKET_DIRNAME
    bucket_path.exists() and bucket_path.rmdir()
    assert bucket_path.exists() == False

    bucket = storage.Bucket(BUCKET_DIRNAME, auto_create_dirs=False)
    logger.info(f'{bucket.path = }')
    assert bucket.path == bucket_path
    assert bucket.path.exists() == False


def test_blob_dont_create_dirs():
    logger.info(f'{storage.FAKE_BUCKETS_ROOT = }')
    BUCKET_DIRNAME = 'test-bucket'
    BLOB_PATH = 'test/dir/test-blob'

    bucket_path = Path(storage.FAKE_BUCKETS_ROOT) / BUCKET_DIRNAME
    bucket_path.exists() and shutil.rmtree(bucket_path)
    assert bucket_path.exists() == False

    bucket = storage.Bucket(BUCKET_DIRNAME, auto_create_dirs=False)
    logger.info(f'{bucket.path = }')
    blob = bucket.blob(BLOB_PATH)
    logger.info(f'{blob.path = }')
    assert blob.path == bucket_path / BLOB_PATH
    assert blob.path.exists() == False
    assert blob.path.parent.exists() == False


def test_blob_auto_create_dirs():
    logger.info(f'{storage.FAKE_BUCKETS_ROOT = }')
    BUCKET_DIRNAME = 'test-bucket'
    BLOB_PATH = 'test/dir/test-blob'

    bucket_path = Path(storage.FAKE_BUCKETS_ROOT) / BUCKET_DIRNAME
    bucket_path.exists() and shutil.rmtree(bucket_path)
    assert bucket_path.exists() == False

    bucket = storage.Bucket(BUCKET_DIRNAME, auto_create_dirs=True)
    logger.info(f'{bucket.path = }')

    blob = bucket.blob(BLOB_PATH)
    logger.info(f'{blob.path = }')
    assert blob.path == bucket_path / BLOB_PATH
    assert blob.path.exists() == False
    assert blob.path.parent.exists() == True
    remove = bucket.path / Path(BLOB_PATH).parts[0]
    shutil.rmtree(remove)
    
    # blob.path.parent.rmdir()
    # bucket.path.exists() and bucket.path.rmdir()
    bucket.path.rmdir()
    
