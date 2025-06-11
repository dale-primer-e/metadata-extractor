from pathlib import Path
from typing import Dict, List, Any
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

from .config import Config
from .exceptions import UnsupportedFormatError


class MetadataExtractor:
    """
    Main class for extracting metadata from image files.

    Handles validation, file system metadata extraction, EXIF metadata parsing,
    and batch processing.
    """

    def __init__(self, config: Config):
        """
        Initialize the extractor with a given configuration.

        Args:
            config (Config): Configuration object containing extraction settings,
                             such as max file size and supported formats.
        """
        self.config = config


    def extract_metadata(self, image_path: Path) -> Dict[str, Any]:
        """
        Extract and return metadata from a single image file.

        Args:
            image_path (Path): Path to the image file.

        Returns:
            Dict[str, Any]: Combined and cleaned metadata from file system and EXIF data.

        Raises:
            FileNotFoundError, UnsupportedFormatError
        """
        self._validate_file(image_path)

        metadata = {}
        metadata.update(self._extract_file_metadata(image_path))
        metadata.update(self._extract_exif_metadata(image_path))

        return self._clean_metadata(metadata)


    def _validate_file(self, path: Path) -> None:
        """
        Validate the file before metadata extraction.

        Checks for file existence, size constraints, and supported format.

        Args:
            path (Path): Path to the image file.

        Raises:
            FileNotFoundError: If file does not exist.
            UnsupportedFormatError: If file format is not supported.
        """
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")

        if path.suffix.lower() not in self.config.supported_formats:
            raise UnsupportedFormatError(f"Unsupported format: {path.suffix}")


    def _extract_file_metadata(self, path: Path) -> Dict[str, Any]:
        """
        Extract basic file system metadata from the image.

        Args:
            path (Path): Path to the image file.

        Returns:
            Dict[str, Any]: Metadata including filename, size, creation and modification times.
        """
        stats = path.stat()
        return {
            'filename': path.name,
            'size': stats.st_size,
            'created_time': datetime.fromtimestamp(stats.st_birthtime).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'modified_time': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }


    def _extract_exif_metadata(self, path: Path) -> Dict[str, Any]:
        """
        Extract EXIF metadata from the image, if present.

        Args:
            path (Path): Path to the image file.

        Returns:
            Dict[str, Any]: Parsed EXIF metadata. Returns an empty dict if extraction fails or no EXIF data is present.
        """
        try:
            with Image.open(path) as img:
                exif_data = img.getexif()
                return self._parse_exif_tags(exif_data) if exif_data else {}
        except Exception:
            return {}


    def _parse_exif_tags(self, exif_data: dict) -> Dict[str, Any]:
        """
        Parse selected EXIF tags into a structured metadata dictionary.

        Args:
            exif_data (dict): Raw EXIF data from the image.

        Returns:
            Dict[str, Any]: Normalized metadata with readable keys (e.g., 'camera_model', 'capture_time').
        """
        metadata = {}

        tag_mapping = {
            'Orientation': 'orientation',
            'DateTime': 'capture_time',
            'Model': 'camera_model',
            'BodySerialNumber': 'camera_serial'
        }

        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name in tag_mapping:
                metadata[tag_mapping[tag_name]] = value

        return metadata


    def _clean_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean metadata dictionary by removing entries with None values.

        Args:
            metadata (Dict[str, Any]): Raw metadata dictionary.

        Returns:
            Dict[str, Any]: Cleaned metadata with non-null values only.
        """
        return {k: v for k, v in metadata.items() if v is not None}


    def process_images(self, image_paths: List[Path]) -> Dict[str, Any]:
        """
        Process a list of images and extract metadata from each.

        Args:
            image_paths (List[Path]): List of paths to image files.

        Returns:
            Dict[str, Any]: Summary containing:
                - successful: List of dicts with path and metadata.
                - failed: List of dicts with path and error info.
                - total_count: Total number of images processed.
                - success_count: Number of successful extractions.
                - failed_count: Number of failed extractions.
        """
        results = {
            'successful': [],
            'failed': [],
            'total_count': len(image_paths),
            'success_count': 0,
            'failed_count': 0
        }

        for path in image_paths:
            try:
                metadata = self.extract_metadata(path)
                results['successful'].append({
                    'path': str(path),
                    'metadata': metadata
                })
                results['success_count'] += 1
            except Exception as e:
                results['failed'].append({
                    'path': str(path),
                    'error': str(e),
                    'error_type': type(e).__name__
                })
                results['failed_count'] += 1

        return results
