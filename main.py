import logging
from google.cloud import storage
from util import setup_logger

logger = setup_logger(__name__)

def main():
    print("Hello from google-cloud-storage-mock!")
    client = storage.Client()
    bucket = client.bucket("my-bucket")
    blob = bucket.blob("test/my-blob")
    if blob.exists(client):
        print(blob.size)
    else:
        print("Blob does not exist")


if __name__ == "__main__":
    main()
