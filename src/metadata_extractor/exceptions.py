class MetadataExtractionError(Exception):
    '''Custom exception for metadata extraction errors.'''
    pass

class UnsupportedFormatError(MetadataExtractionError):
    '''Exception raised for unsupported image formats.'''
    pass
