'''
Metatdata Extractor - Extract metadata from image files and print it to JSON files.
'''

from .core import MetadataExtractor
from .config import Config
from .exceptions import MetadataExtractionError, UnsupportedFormatError

__version__ = '1.0.0'
__author__ = 'Dale Euinton'
__email__ = 'dale.euinton@gmail.com'

__all__ = [
    'MetadataExtractor',
    'Config',
    'MetadataExtractionError',
    'UnsupportedFormatError'
]
