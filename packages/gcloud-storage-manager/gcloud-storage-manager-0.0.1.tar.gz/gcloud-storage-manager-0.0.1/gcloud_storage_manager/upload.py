from dataclasses import dataclass, field
from typing import List, Tuple

from tqdm import tqdm

from gcloud_storage_manager.base import BaseStorageFileHandler
from gcloud_storage_manager.std_logging import logging


@dataclass
class UploadResult:
    success_count: int
    failure_count: int
    failed_keys: List[str]
    invalid_keys: List[str] = field(default_factory=list)

    @property
    def has_errors(self):
        return len(self.failed_keys) > 0 or len(self.invalid_keys) > 0


class StorageFileUploader(BaseStorageFileHandler):
    """
    Upload files to cloud storage.

    e.g.
    uploader = StorageFileUploader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType("SVG", ".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )
    result = uploader.upload_files(validated_files)
    """

    def upload_files(
        self,
        validated_files: List[Tuple[str, bytes]],  # (file_path, file_content)
        overwrite: bool = False,
    ) -> UploadResult:
        logging.info("Start of uploading files to cloud storage")

        success_count = 0
        failure_count = 0
        failed_keys: List[str] = []
        with tqdm(total=len(validated_files), desc="Uploading", ncols=80) as pbar:
            for file_path, file_content in validated_files:
                if self._upload_file(file_path, file_content, overwrite):
                    success_count += 1
                else:
                    failed_keys.append(file_path)
                    failure_count += 1
                pbar.update()

        logging.info("End of uploading files to cloud storage")

        return UploadResult(success_count, failure_count, failed_keys)

    def _upload_file(
        self, file_path: str, file_content: bytes, overwrite: bool
    ) -> bool:
        """
        Upload a file to cloud storage.

        e.g.
        file_path = "test_path"
        file_content = b"test_content"
        overwrite = False
        uploader._upload_file(file_path, file_content, overwrite)
        """
        try:
            full_file_path = (
                f"{self.storage_base_dir}/{file_path}{self.file_type.extension}"
            )
            blob = self.bucket.blob(full_file_path)
            if blob.exists() and not overwrite:
                return False
            blob.upload_from_string(
                file_content, content_type=self.file_type.content_type
            )
            return True
        except Exception as e:
            logging.info(f"Error uploading '{full_file_path}': {e}")
            return False
