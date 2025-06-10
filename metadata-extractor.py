#!/usr/bin/env python3
import argparse
import sys
import os
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import json

def extract_metadata(image_path):
    if not os.path.exists(image_path):
        print(f'Error: File not found - {image_path}')
        return None
    
    try:
        file_stats = os.stat(image_path)
        
        metadata = {
            'filename': os.path.basename(image_path),
            'size': file_stats.st_size,
            'created_time': datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'modified_time': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'orientation': None,
            'capture_time': None,
            'camera_model': None,
            'camera_serial': None
        }
        
        with Image.open(image_path) as img:
            exif_data = img.getexif()
            
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    
                    if tag_name == 'Orientation':
                        metadata['orientation'] = value
                    elif tag_name == 'DateTime':
                        metadata['capture_time'] = value
                    elif tag_name == 'Model':
                        metadata['camera_model'] = value
                    elif tag_name == 'BodySerialNumber':
                        metadata['camera_serial'] = value
        
        return metadata
        
    except Exception as e:
        print(f'Error processing {image_path}: {str(e)}')
        return None


def write_metadata_json(metadata, json_path):
    try:
        filtered_dict = {key: value for key, value in metadata.items() if value is not None}
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_dict, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f'Error writing JSON file {json_path}: {str(e)}')
        return False


def parse_args():
    parser = argparse.ArgumentParser(
        description='Extract metadata from image files',
        epilog='Example: python metadata-extractor.py "CAM18839.jpg" "images/CAM18840.jpg" "other/test.jpg"'
    )
    
    parser.add_argument(
        'images',
        nargs='+',
        help='Path(s) to image file(s) to process'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def process_image(image_path):
    metadata = extract_metadata(image_path)
    if metadata:
        json_path = os.path.splitext(image_path)[0] + '.json'
        return write_metadata_json(metadata, json_path)
    else:
        return false


def main():
    args = parse_args()
    success_count = 0
    
    for image_path in args.images:
        if args.verbose:
            print(f'Processing image: {image_path}')

        if process_image(image_path):
            success_count += 1
    
    if success_count == len(args.images):
        return 0
    else: 
        return 1


if __name__ == '__main__':
    sys.exit(main())
