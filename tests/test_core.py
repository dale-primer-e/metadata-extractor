import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from PIL import Image
import os
import tempfile

from src.metadata_extractor.core import MetadataExtractor
from src.metadata_extractor.config import Config
from src.metadata_extractor.exceptions import UnsupportedFormatError

class TestMetadataExtractor:
    
    @pytest.fixture
    def config(self):
        """Create a mock config for testing."""
        config = Mock(spec=Config)
        config.max_file_size = 10 * 1024 * 1024  # 10MB
        config.supported_formats = ['.jpg', '.jpeg', '.png', '.tiff']
        return config
    
    @pytest.fixture
    def extractor(self, config):
        """Create MetadataExtractor instance."""
        return MetadataExtractor(config)
    
    @pytest.fixture
    def mock_image_file(self):
        """Create a temporary image file for testing."""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            img = Image.new('RGB', (1, 1), color='red')
            img.save(tmp_file.name, 'JPEG')
            yield Path(tmp_file.name)

        # Cleanup
        try:
            os.unlink(tmp_file.name)
        except FileNotFoundError:
            pass
    
    def test_extract_metadata_success(self, extractor, mock_image_file):
        with patch.object(Path, 'stat') as mock_stat, patch('PIL.Image.open') as mock_open:
            mock_stat_result = Mock()
            mock_stat_result.st_size = 1024  # 1KB
            mock_stat_result.st_birthtime = 1640995200.0  # 2022-01-01 00:00:00
            mock_stat_result.st_mtime = 1640995200.0
            mock_stat.return_value = mock_stat_result

            mock_image = Mock()
            mock_exif = {
                'Model': 'Model1', 
                'DateTime': 'mocked date', 
                'Orientation': 'horizontal', 
                'BodySerialNumber': '123'
            }
            mock_image.getexif.return_value = mock_exif
            mock_open.return_value.__enter__.return_value = mock_image
            
            result = extractor.extract_metadata(mock_image_file)
            
            assert 'filename' in result
            assert 'size' in result
            assert 'created_time' in result
            assert 'modified_time' in result
            assert 'camera_model' in result
            assert 'capture_time' in result
            assert 'orientation' in result
            assert 'camera_serial' in result
            assert result['filename'] == mock_image_file.name
            assert result['size'] == 1024
            assert result['created_time'] == '2022-01-01T13:00:00.000000Z'
            assert result['modified_time'] == '2022-01-01T13:00:00.000000Z'
            assert result['camera_model'] == 'Model1'
            assert result['capture_time'] == 'mocked date'
            assert result['orientation'] == 'horizontal'
            assert result['camera_serial'] == '123'
    
    def test_extract_metadata_file_not_found(self, extractor):
        non_existent_path = Path('/non/existent/file.jpg')
        
        with pytest.raises(FileNotFoundError, match="File does not exist"):
            extractor.extract_metadata(non_existent_path)
    
    def test_extract_metadata_unsupported_format(self, extractor):
        with tempfile.NamedTemporaryFile(suffix='.bmp', delete=False) as tmp_file:
            unsupported_path = Path(tmp_file.name)

            with patch.object(Path, 'stat') as mock_stat:
                mock_stat_result = Mock()
                mock_stat_result.st_size = 1024  # 1KB
                mock_stat.return_value = mock_stat_result

                try:
                    with pytest.raises(UnsupportedFormatError, match="Unsupported format"):
                        extractor.extract_metadata(unsupported_path)
                    tmp_file.close()
                finally:
                    # Cleanup
                    try:
                        os.unlink(tmp_file.name)
                    except FileNotFoundError:
                        pass
