import logging
from pathlib import Path
import shutil
import pytest
from google.cloud import storage

logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(module)10s | %(funcName)15s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

BUCKET_DIRNAME = 'test-bucket'

@pytest.fixture
def test_bucket(request):
    """
    A fixture that provides a Bucket instance for testing.

    It is designed to be used with indirect parametrization to control the
    `auto_create_dirs` flag. It handles the creation and reliable teardown
    of the bucket's temporary directory.

    The yielded value is the configured `Bucket` instance.
    """
    # Use request.param to get the value from @pytest.mark.parametrize
    auto_create_dirs = request.param

    bucket_path = Path(storage.FAKE_BUCKETS_ROOT) / BUCKET_DIRNAME

    # Ensure a clean state before the test runs
    if bucket_path.exists():
        shutil.rmtree(bucket_path)

    bucket = storage.Bucket(BUCKET_DIRNAME, auto_create_dirs=auto_create_dirs)

    yield bucket

    # Teardown: This code runs after the test is complete
    if bucket_path.exists():
        shutil.rmtree(bucket_path)


def test_sys_path():
    import sys
    logger.info(sys.path)


@pytest.mark.parametrize('test_bucket', [True], indirect=True)
def test_new_bucket_auto_create_dirs(test_bucket):
    logger.info(f'{test_bucket.path = }')
    assert test_bucket.path.exists()
    assert test_bucket.path.is_dir()


@pytest.mark.parametrize('test_bucket', [False], indirect=True)
def test_new_bucket_dont_create_dirs(test_bucket):
    logger.info(f'{test_bucket.path = }')
    assert not test_bucket.path.exists()


@pytest.mark.parametrize('test_bucket', [False], indirect=True)
def test_blob_dont_create_dirs(test_bucket):
    BLOB_PATH = 'test/dir/test-blob'
    blob = test_bucket.blob(BLOB_PATH)
    logger.info(f'{blob.path = }')
    assert not blob.path.exists()
    assert not blob.path.parent.exists()


@pytest.mark.parametrize('test_bucket', [True], indirect=True)
def test_blob_auto_create_dirs(test_bucket):
    BLOB_PATH = 'test/dir/test-blob'
    blob = test_bucket.blob(BLOB_PATH)
    logger.info(f'{blob.path = }')
    assert not blob.path.exists()
    assert blob.path.parent.exists()
    
