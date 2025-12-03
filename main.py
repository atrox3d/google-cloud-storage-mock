import logging
logging.basicConfig(level=logging.INFO)

from google.cloud import storage

logger = logging.getLogger(__name__)

def main():
    print("Hello from google-cloud-storage-mock!")


if __name__ == "__main__":
    main()
