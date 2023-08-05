from unittest.mock import patch

import pytest

from gcloud_storage_manager import FileType, StorageFileUploader, UploadResult


def test_upload_result():
    result = UploadResult(
        success_count=5, failure_count=2, failed_keys=["key1", "key2"]
    )

    # 成功数と失敗数をテスト
    assert result.success_count == 5
    assert result.failure_count == 2

    # 失敗したキーをテスト
    assert len(result.failed_keys) == 2
    assert "key1" in result.failed_keys
    assert "key2" in result.failed_keys

    # invalid_keys がデフォルトで空であることをテスト
    assert result.invalid_keys == []

    # has_errors のテスト
    assert result.has_errors is True

    # エラーがない場合のhas_errorsをテスト
    result_no_error = UploadResult(success_count=5, failure_count=0, failed_keys=[])
    assert result_no_error.has_errors is False


@patch("google.cloud.storage.Client")
@patch("google.cloud.storage.Bucket")
@patch("google.cloud.storage.Blob")
def test_upload_file(mock_blob, mock_bucket, mock_storage_client):
    mock_storage_client.from_service_account_json.return_value = mock_storage_client
    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob
    mock_blob.exists.return_value = False

    uploader = StorageFileUploader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType("SVG", ".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )

    uploader._upload_file("test_key", b"test bytes", False)

    mock_bucket.blob.assert_called_once_with("test_dir/test_child_dir/test_key.svg")
    mock_blob.upload_from_string.assert_called_once_with(
        b"test bytes", content_type="image/svg+xml"
    )


@pytest.fixture
def mock_upload_file():
    with patch.object(StorageFileUploader, "_upload_file", return_value=True) as _mock:
        yield _mock


@patch("google.cloud.storage.Client")
def test_upload_files(mock_storage_client, mock_upload_file):
    mock_storage_client.from_service_account_json.return_value = mock_storage_client

    uploader = StorageFileUploader(
        bucket_name="test_bucket",
        dir_name="test_dir",
        dir_name_child="test_child_dir",
        file_type=FileType("SVG", ".svg", "image/svg+xml"),
        credentials_path="path/to/creds.json",
    )

    validated_files = [("test_key1", b"test bytes1"), ("test_key2", b"test bytes2")]
    result = uploader.upload_files(validated_files, False)

    assert mock_upload_file.call_count == len(validated_files)
    for file in validated_files:
        mock_upload_file.assert_any_call(*file, False)

    assert result.success_count == len(validated_files)
    assert result.failure_count == 0
    assert result.failed_keys == []
    assert not result.has_errors
