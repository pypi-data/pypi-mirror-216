from typing import NamedTuple

from google.cloud import storage


class FileType(NamedTuple):
    """
    File type information.

    e.g.
    FileType("SVG", ".svg", "image/svg+xml")
    """

    label: str
    extension: str
    content_type: str


class BaseStorageFileHandler:
    def __init__(
        self,
        bucket_name: str,
        dir_name: str,
        dir_name_child: str,
        file_type: FileType,
        credentials_path: str,
    ):
        self.file_type = file_type
        self.storage_client = storage.Client.from_service_account_json(credentials_path)
        self.bucket = self.storage_client.bucket(bucket_name)
        self.storage_base_dir = f"{dir_name}/{dir_name_child}"

    def _file_match(self, file_name: str) -> bool:
        return file_name.endswith(self.file_type.extension)
