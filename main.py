import logging
logging.basicConfig(
    format='%(asctime)s | %(levelname)-8s | %(funcName)20s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
from google.cloud import storage

logger = logging.getLogger(__name__)

def main():
    print("Hello from google-cloud-storage-mock!")
    client = storage.Client()
    bucket = client.bucket("my-bucket")
    blob = bucket.blob("my-blob")

if __name__ == "__main__":
    main()
