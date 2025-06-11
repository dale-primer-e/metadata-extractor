import os.path
from pathlib import Path
from src.metadata_extractor.utils import get_json_path

class TestGetJsonPath:
    def test_get_json_path_returns_json_path(self):
        image_path = Path("example.jpg")
        expected = "example.json"
        result = str(get_json_path(image_path))
        assert result == expected

    def test_get_json_path_without_suffix_returns_json_path(self):
        image_path = Path("example")
        expected = "example.json"
        result = str(get_json_path(image_path))
        assert result == expected

    def test_get_json_path_with_complex_filename_returns_json_path(self):
        image_path = Path("folder/photo.image.jpeg")
        expected = os.path.join("folder", "photo.image.json")
        result = str(get_json_path(image_path))
        assert result == expected
