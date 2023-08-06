from azure.storage.blob import BlobServiceClient, ContentSettings, __version__
from azure.core import exceptions
from os import path, remove
from django_utils.local_file import write_file
from typing import BinaryIO
from django.conf import settings
from django_utils.logger_app import get_logger
import tempfile

BUCKET_NAME = settings.BUCKET_NAME

class BlobStorage:

    def __init__(self) -> None:
        self.logger = get_logger('AzureBlobStorage')
        try:
            self.logger.info(f"Azure Blob Storage v{__version__}")
            connection_string = settings.BLOB_STORAGE_CONNECTION_STRING
            self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            self.container_client = self.blob_service_client.create_container(name=BUCKET_NAME, public_access='blob')

        except exceptions.ResourceExistsError as ex:
            self.logger.info(f"Container '{BUCKET_NAME}' already exists")

        except Exception as ex:
            self.logger.error(ex)

    def save_file(self, file, content_type) -> str:
        file_name = write_file(file, content_type)
        file_path = path.join(tempfile.gettempdir(), file_name)
        temp_file = open(file_path, mode='rb')
        self.upload_blob(temp_file, file_name, content_type)
        temp_file.close()
        remove(file_path)
        return file_name

    def upload_blob(self, source_file_name: BinaryIO, destination_blob_name: str, blob_type: str):
        blob_client = self.blob_service_client.get_blob_client(container=BUCKET_NAME, blob=destination_blob_name)

        # Upload the created file
        content_settings = ContentSettings(content_type=blob_type)
        blob_client.upload_blob(source_file_name, content_settings=content_settings)

        self.logger.info(f"File {source_file_name} uploaded to container {BUCKET_NAME}: {destination_blob_name}")

    def delete_blob(self, blob_name: str):
        blob_name = blob_name.replace(self.get_url_prefix(), "")

        blob_client = self.blob_service_client.get_blob_client(container=BUCKET_NAME, blob=blob_name)

        blob_client.delete_blob()

        self.logger.info(f"Blob {blob_name} deleted.")

    def get_url_prefix(self) -> str:
        return f"https://{settings.AZURE_STORAGE_ACCOUNT}.blob.core.windows.net/{BUCKET_NAME}/"


blob_storage = BlobStorage()