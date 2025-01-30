# Gigapan Tile Downloader & Assembler

## Overview
This project allows users to download and assemble tiles from Gigapan images. It supports multithreaded tile downloading and automatic image reconstruction.

## Features
- Download tiles from Gigapan using multithreading.
- Assemble downloaded tiles into a complete image.
- Queue system for processing multiple photo IDs.
- Logging for debugging and progress tracking.
- Interactive menu for ease of use.

## Requirements
Ensure you have the following dependencies installed:

```sh
pip install opencv-python numpy tqdm
```

## Usage
Run the script and follow the interactive menu:

```sh
python script.py
```

### Menu Options:
1. **Download tiles only**: Fetch tiles for a given photo ID.
2. **Assemble image only**: Reconstruct an image from downloaded tiles.
3. **Download and assemble**: Perform both steps automatically.
4. **Process the queue**: Process multiple photo IDs stored in a queue.
5. **Add photo IDs to queue**: Queue photo IDs for later processing.
6. **View queue**: Display the current queue.
7. **Exit**: Close the program.

## File Structure
- `queue.txt` - Stores queued photo IDs.
- `tiles/` - Directory where tiles are downloaded.
- `{photo_id}_assembled.tiff` - Final assembled image.

## Example
To download and assemble a Gigapan image with ID `123456`:

1. Run the script.
2. Select option `3` (Download and assemble).
3. Enter `123456` as the photo ID.
4. The assembled image will be saved as `123456_assembled.tiff`.

## License
This project is released under the MIT License.

