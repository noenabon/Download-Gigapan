# Gigapan Image Downloader & Stitcher

## Overview
Gigapan Image Downloader & Stitcher is a Python-based tool designed for downloading high-resolution Gigapan image tiles and assembling them seamlessly. Utilizing OpenCV and multithreading, it ensures fast tile retrieval and efficient image reconstruction. This tool is ideal for processing large-scale panoramic images with automated stitching capabilities.

## Features
- Fast multithreaded tile downloading from Gigapan.
- Automated image stitching using OpenCV.
- Queue system for batch processing multiple photo IDs.
- Detailed logging for tracking progress and debugging.
- User-friendly interactive menu for streamlined operation.

## Installation Guide
Ensure you have the required dependencies installed:

```sh
pip install opencv-python numpy tqdm
```

## Usage
Run the script and follow the interactive menu:

```sh
python script.py
```

### Menu Options:
1. **Download tiles only**: Fetch tiles for a specific photo ID.
2. **Assemble image only**: Construct an image from downloaded tiles.
3. **Download and assemble**: Perform both steps in sequence.
4. **Process the queue**: Handle multiple queued photo IDs automatically.
5. **Add photo IDs to queue**: Store photo IDs for later processing.
6. **View queue**: Display queued photo IDs.
7. **Exit**: Close the program.

## File Structure
- `queue.txt` - Stores queued photo IDs.
- `tiles/` - Directory containing downloaded tiles.
- `{photo_id}_assembled.tiff` - Final stitched image output.

## Why Use This Tool?
- **Efficient Processing**: Multithreading accelerates tile downloads.
- **High-Quality Stitching**: OpenCV ensures seamless image assembly.
- **Automation**: Queue system allows batch processing of images.
- **Easy to Use**: Simple interactive menu for all functions.

## Example
To download and assemble a Gigapan image with ID `123456`:

1. Run the script.
2. Select option `3` (Download and assemble).
3. Enter `123456` as the photo ID.
4. The assembled image will be saved as `123456_assembled.tiff`.

## License
This project is released under the MIT License.

