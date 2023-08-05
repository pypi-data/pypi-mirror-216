from unittest.mock import Mock, patch

from google.api_core.exceptions import GoogleAPIError
from google.cloud import storage

from gcloud_storage_manager import FileType, StorageFileDownloader


@patch("google.cloud.storage.Client")
def test__file_match(mock_storage_client):
    mock_storage_client.from_service_account_json.return_value = mock_storage_client

    downloader = StorageFileDownloader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType("SVG", ".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )

    assert downloader._file_match("test_file.svg") is True
    assert downloader._file_match("test_file.jpg") is False


@patch("google.cloud.storage.Client")
def test_load_files_by_key(mock_storage_client):
    # Create a mock Blob object to return as part of our mocked bucket.list_blobs
    mock_blob = Mock(spec=storage.Blob)
    mock_blob.download_as_bytes.return_value = b"test bytes"
    mock_blob.name = "test_file.svg"

    # Mock the storage Client's from_service_account_json
    mock_storage_client.from_service_account_json.return_value.bucket.return_value.list_blobs.return_value = [
        mock_blob
    ]

    downloader = StorageFileDownloader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType("SVG", ".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )

    result = downloader.load_files_by_key("test_char")

    assert len(result) == 1
    assert result[0] == b"test bytes"


@patch("google.cloud.storage.Client")
def test_load_files_all(mock_storage_client):
    # Create a mock Blob object to return as part of our mocked bucket.list_blobs
    mock_blob = Mock(spec=storage.Blob)
    mock_blob.download_as_bytes.return_value = b"test bytes"
    mock_blob.name = "test_file.svg"

    # Mock the storage Client's from_service_account_json
    mock_storage_client.from_service_account_json.return_value.bucket.return_value.list_blobs.return_value = [
        mock_blob
    ]

    downloader = StorageFileDownloader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType("SVG", ".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )

    result = downloader.load_files_all(["test_char", "test_char_2"])

    assert len(result) == 2
    assert all(len(v) == 1 for v in result.values())
    assert all(v[0] == b"test bytes" for v in result.values())


@patch("google.cloud.storage.Client")
def test__file_match_failed(mock_storage_client):
    mock_storage_client.from_service_account_json.return_value = mock_storage_client

    downloader = StorageFileDownloader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType("SVG", ".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )

    assert downloader._file_match("test_file.svg") is True
    assert downloader._file_match("test_file.jpg") is False


@patch("google.cloud.storage.Client")
def test_load_files_all_handle_api_error(mock_storage_client):
    # Create a mock Blob object to return as part of our mocked bucket.list_blobs
    mock_blob = Mock(spec=storage.Blob)
    mock_blob.download_as_bytes.side_effect = GoogleAPIError("test error")
    mock_blob.name = "test_file.svg"

    # Mock the storage Client's from_service_account_json
    mock_storage_client.from_service_account_json.return_value.bucket.return_value.list_blobs.return_value = [
        mock_blob
    ]

    downloader = StorageFileDownloader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType("SVG", ".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )

    keys = ["test_char1", "test_char2"]
    result = downloader.load_files_all(keys)

    assert all(len(files) == 0 for files in result.values())
