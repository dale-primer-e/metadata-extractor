from pathlib import Path
import json
import os

def get_json_path(image_path: Path) -> Path:
    """
    Generate the corresponding JSON file path for a given image path.

    Args:
        image_path (Path): Path to the image file.

    Returns:
        Path: New Path object with the same base name as the image but with a '.json' extension.
    """
    path = str(image_path)
    output_path = os.path.splitext(path)[0] + '.json'
    return Path(output_path)

def write_json(data: dict[str, any], output_path: Path) -> None:
    """
    Serialize a dictionary to a JSON file at the specified path.

    Args:
        data (dict[str, any]): Dictionary containing data to write to JSON.
        output_path (Path): Destination path for the JSON output file.

    Notes:
        - Writes with UTF-8 encoding.
        - Uses 2-space indentation for readability.
        - Serializes non-serializable objects using str().
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
