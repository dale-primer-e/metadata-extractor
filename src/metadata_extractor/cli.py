import argparse
import sys
from pathlib import Path
from typing import List
from .core import MetadataExtractor
from .config import Config
from .utils import get_json_path, write_json


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and returns a configured argument parser for the metadata extraction CLI.

    Returns:
        argparse.ArgumentParser: Configured parser with the following arguments:
        
            - images (positional): One or more paths to image files to process.

    Notes:
        - Supports multiple image inputs in one invocation.
    """
    parser = argparse.ArgumentParser(
        description='Extract metadata from image files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('images', nargs='+', help='Path(s) to image file(s) to process')
    
    return parser


def validate_inputs(image_paths: List[str]) -> List[Path]:
    """
    Validates a list of image file paths and returns only those that exist and are files.

    Args:
        image_paths (List[str]): List of input file paths as strings.

    Returns:
        List[Path]: List of valid image paths as pathlib.Path objects.

    Notes:
        - Prints a warning for each path that does not exist or is not a file.
        - Skips invalid paths silently (aside from printed warnings).
    """
    valid_paths = []
    for path in image_paths:
        path = Path(path)
        if not path.exists():
            print(f"Warning: {path} does not exist, skipping")
            continue
        if not path.is_file():
            print(f"Warning: {path} is not a file, skipping")
            continue
        valid_paths.append(path)
    return valid_paths


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        config = Config()
        image_paths = validate_inputs(args.images)
        
        extractor = MetadataExtractor(config)
        results = extractor.process_images(image_paths)

        for result in results['successful']:
            json_path = get_json_path(result['path'])
            write_json(result['metadata'], json_path)

        print(f'Successful: {results['success_count']} Failures: {results['failed_count']}')
        for failure in results['failed']:
            print(f'{failure['path']} - {failure['error_type']} - {failure['error']}')

        return 0 if results['failed_count'] == 0 else 1
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 130
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
