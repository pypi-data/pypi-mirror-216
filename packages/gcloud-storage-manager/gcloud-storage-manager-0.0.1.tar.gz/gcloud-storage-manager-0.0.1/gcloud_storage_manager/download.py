from typing import Dict, List

from google.api_core.exceptions import GoogleAPIError
from google.cloud import storage
from tqdm import tqdm

from gcloud_storage_manager.base import BaseStorageFileHandler
from gcloud_storage_manager.std_logging import logging


class StorageFileDownloader(BaseStorageFileHandler):
    """
    Download files from cloud storage.

    e.g.
    downloader = StorageFileDownloader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType("SVG", ".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )
    files = downloader.load_files_by_key("test_key")
    """

    def load_files_all(self, keys: List[str]) -> Dict[str, List[bytes]]:
        """
        Load files from cloud storage.

        e.g.
        keys = ["key1", "key2", "key3"]
        files = downloader.load_files_all(keys)
        """
        results: Dict[str, List[bytes]] = {}

        logging.info("Start of getting files from cloud storage")
        with tqdm(total=len(keys), desc="Uploading", ncols=80) as pbar:
            for key in keys:
                try:
                    results[key] = self.load_files_by_key(key)
                except GoogleAPIError as e:
                    logging.info(
                        f"Failed to download {self.file_type.label} "
                        f"data for '{key}': {e}"
                    )
                    results[key] = []
                pbar.update()

        logging.info("Finish of getting files from cloud storage")

        return results

    def load_files_by_key(self, key: str) -> List[bytes]:
        """
        Load files from cloud storage.

        e.g.
        key = "test_key"
        files = downloader.load_files_by_key(key)
        """
        file_path_prefix = f"{self.storage_base_dir}/{key}"
        blobs = self.bucket.list_blobs(prefix=file_path_prefix)
        files = []
        for blob_ in blobs:
            blob: storage.Blob = blob_
            file_name: str = blob.name
            if self._file_match(file_name):
                files.append(blob.download_as_bytes())
        return files
