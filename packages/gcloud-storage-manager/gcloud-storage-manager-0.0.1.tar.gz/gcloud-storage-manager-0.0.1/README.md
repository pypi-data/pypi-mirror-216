Usage: See the codes in tests/ directory.

# install
```
pip install gcloud_storage_manager
```

# usage
## download
```
from src.infra.storage import FileType, StorageFileDownloader

downloader = StorageFileDownloader(
    bucket_name="test_bucket",
    dir_name="test_dir",
    dir_name_child="test_child_dir",
    file_type=FileType("SVG", ".svg", "image/svg+xml"),
    credentials_path="path/to/creds.json",
)

keys = ["test_char1", "test_char2"]
result = downloader.load_files_all(keys)
```

## upload
```
from src.infra.storage import FileType, StorageFileUploader

uploader = StorageFileUploader(
    bucket_name="test_bucket",
    dir_name="test_dir",
    dir_name_child="test_child_dir",
    file_type=FileType("SVG", ".svg", "image/svg+xml"),
    credentials_path="path/to/creds.json",
)

uploader._upload_file("test_key", b"test bytes", False)
```

# prerequest
- program can read gcloud json key file from the project environment
- gcloud storage api is activated and backet is already created

