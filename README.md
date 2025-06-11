# Image Metadata Extractor

Extract a fixed set of metadata from image files, including filesystem attributes and embedded EXIF data, with configurable file size and format restrictions.

## To-Do

I would have liked to have: 

- More tests, especially for edge cases (the testing is minimal and could be improved)
- Finish of the module so it's installable with pip 
- Move the print statements into proper logging

## Features

* Validate image paths and file formats
* Extract **LIMITED** filesystem metadata (filename, size, timestamps)
* Extract and parse **LIMITED** EXIF metadata (camera model, capture time, orientation, etc.)
* Process multiple images in batch mode
* Export metadata as JSON files

## Usage

Clone the project and then inside the main project folder `metadata-extractor`

Run:

```powershell
python -m src.metadata_extractor image1.jpg image2.jpg
```

### Arguments

* `images`: One or more image file paths to process (must be jpg)

## Output

Metadata is saved as JSON files named after each image, e.g., `image1.json`.

## Error Handling

* Invalid or missing files are skipped with warnings.
* Unsupported formats raise errors.
* Errors for individual files do not stop batch processing.

## Configuration

Adjust settings in the `Config` object, including:

* Supported image formats (e.g., `.jpg`)

## Development

* Python 3.8+
* Uses `Pillow` for image processing
* Standard libraries: `pathlib`, `argparse`, `json`

# Description of task

**Note:** I checked about not using Rust and it's fine.

## Narrative Rust Test (Metadata)

### Overview

This test will be used to assess your ability to write software using the Rust programming language.

Please spend a maximum of 4 hours on this problem. We are looking for quality, not quantity. If you run out of time, consider creating a quick to-do list of things you would want to improve / change.

Please use git to track the changes you make as you develop your solution and submit either a zip file containing a clone of the repository, or a link to the repository on a public host such as Github, GitLab or Bitbucket.

### Task

Your task is to create a command-line application that extracts a fixed set of metadata from one or more JPEG images specified on the command line, and serializes the data for each to a JSON file. Start by extracting the following fields from the filesystem metadata:

- `filename`
- `size (Bytes)`
- `created_time`
- `modified_time`

In addition to the basic filesystem metadata, you should extract the following EXIF fields from each image:

- `orientation` (Exif.Image.Orientation)
- `capture_time` (Exif.Image.DateTimeOriginal)
- `camera_model` (Exif.Image.Model)
- `camera_serial` (Exif.Image.BodySerialNumber)

The output JSON document will be a text file with a top-level JSON object containing each of the property values for the file. The output file name will be the input file name with .json as its extension (replacing the input file's .jpg or .jpeg extension). Numeric values should be serialized as numbers, text values should be serialized as strings, and date/time values should be serialized as strings in a valid ISO-8601 format (either UTC or local). Any unspecified or unavailable values should be omitted in the output.

You can use any publicly available Rust libraries in completing this task, but the following libraries are suggested as a starting point:

- kamdak-exif
- serde_json
- chrono

Example

If the input to the application is:

```
./your-app "images/CAM18839.jpg" 
```

The output JSON document might be:

```
{ 	"filename": "CAM18839.jpg", 	"size": 1164980, 	"created_time": "2020-08-13T10:57:06.773358405Z", 	"modified_time": "2020-08-13T10:57:06.773358405Z", 	"orientation": 1, 	"capture_time": "2020-08-09T12:58:32", 	"camera_model": "EOS 5D Mark IV", 	"camera_serial": "025021000535" } 
```

The filename for this output document should be CAM18839.json and it should be located in the same directory as the input image (images).

If the input to the application was:

```
./your-app "images/CAM18839.jpg" "images/CAM18840.jpg" "other/test.jpg" 
```

We would expect to see the application output a total of 3 JSON documents at the locations images/CAM18839.json, images/CAM18830.json and other/test.json.

### Testing

Included with this document is a zip file containing a collection of images you can use to test your application manually.

Treat this like a production piece of software. We encourage you to show us the things you deem important in building a production level piece of software, be it tests, benchmarks, documentation, error handling, performance tuning etc.

We expect this test to be written in Rust: show us what you know about the language, or document parts you're unsure about. You may use any libraries you wish, as long as the source code for them is publicly available.

