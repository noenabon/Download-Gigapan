import os
import sys
import math
import logging
import time
import cv2
from urllib.request import urlopen
from xml.dom.minidom import parseString
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import numpy as np

# Configure logging for better control
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def get_text(nodelist):
    """Extract text from XML node."""
    return "".join(node.data for node in nodelist if node.nodeType == node.TEXT_NODE)

def find_element_value(element, name):
    """Find the value of an element by name in the XML tree."""
    nodes = [element]
    while nodes:
        node = nodes.pop()
        if node.nodeType == node.ELEMENT_NODE and node.localName == name:
            return get_text(node.childNodes)
        nodes.extend(node.childNodes)
    return None

def assemble_tiles(photo_id, width, height, tile_size):
    """Assemble all tiles into a single image."""
    tiles_path = os.path.join(str(photo_id), "tiles")
    final_image = np.zeros((height, width, 3), dtype=np.uint8)

    for j in range((height // tile_size) + 1):
        for i in range((width // tile_size) + 1):
            tile_filename = os.path.join(tiles_path, f"{j:04d}-{i:04d}.png")
            if os.path.exists(tile_filename):
                tile = cv2.imread(tile_filename, cv2.IMREAD_UNCHANGED)
                if tile is None:
                    logging.error(f"Failed to load tile: {tile_filename}")
                    continue

                x, y = i * tile_size, j * tile_size
                tile_h = min(tile.shape[0], final_image.shape[0] - y)
                tile_w = min(tile.shape[1], final_image.shape[1] - x)
                final_image[y:y + tile_h, x:x + tile_w] = tile[:tile_h, :tile_w]

    output_filename = os.path.join(str(photo_id), f"{photo_id}_assembled.tiff")
    cv2.imwrite(output_filename, final_image)
    logging.info(f"Final image saved as {output_filename}")

def download_tile(j, i, photo_id, base, maxlevel, tile_size, tiles_path):
    """Download a single tile."""
    filename = os.path.join(tiles_path, f"{j:04d}-{i:04d}.png")
    if os.path.isfile(filename):
        logging.debug(f"Tile {filename} already exists. Skipping download.")
        return

    url = f"{base}/get_ge_tile/{photo_id}/{maxlevel}/{j}/{i}"
    try:
        with urlopen(url) as response, open(filename, "wb") as fout:
            fout.write(response.read())
        logging.debug(f"Tile downloaded: {filename}")
    except Exception as e:
        logging.error(f"Error downloading tile {filename}: {e}")

def get_tiles(photo_id, base, maxlevel, wt, ht, tile_size):
    """Download all tiles for the given photo ID."""
    tiles_path = os.path.join(str(photo_id), "tiles")
    os.makedirs(tiles_path, exist_ok=True)

    total_tiles = wt * ht
    with ThreadPoolExecutor(max_workers=20) as executor:
        with tqdm(total=total_tiles, desc="Downloading tiles", unit="tile") as pbar:
            futures = [
                executor.submit(download_tile, j, i, photo_id, base, maxlevel, tile_size, tiles_path)
                for j in range(ht) for i in range(wt)
            ]
            for future in futures:
                future.add_done_callback(lambda _: pbar.update(1))
            for future in futures:
                future.result()

def get_photoid():
    """Retrieve photo ID from command line or user input."""
    try:
        return int(sys.argv[1])
    except IndexError:
        return int(input("Enter photo ID: "))

def remove_first_line(file_path):
    """Remove the first line of a file."""
    with open(file_path, "r") as file:
        lines = file.readlines()
    with open(file_path, "w") as file:
        file.writelines(lines[1:])

def add_to_queue(photo_ids):
    """Add photo IDs to the queue file."""
    queue_file = "queue.txt"
    existing_ids = set()
    if os.path.exists(queue_file):
        with open(queue_file, "r") as file:
            existing_ids = set(line.strip() for line in file)

    with open(queue_file, "a") as file:
        for photo_id in photo_ids:
            if str(photo_id) not in existing_ids:
                file.write(f"{photo_id}\n")
                logging.info(f"Photo ID {photo_id} added to the queue.")

def view_queue():
    """View the contents of the queue."""
    queue_file = "queue.txt"
    if os.path.exists(queue_file) and os.path.getsize(queue_file) > 0:
        with open(queue_file, "r") as file:
            queue = file.readlines()
        print("\n--- Current Queue ---")
        for i, photo_id in enumerate(queue, start=1):
            print(f"{i}. {photo_id.strip()}")
    else:
        print("\nThe queue is empty.")

# Main program logic
base = "http://www.gigapan.org"

while True:
    print("\n--- Menu ---")
    print("1. Download tiles only")
    print("2. Assemble image only")
    print("3. Download and assemble")
    print("4. Process the queue")
    print("5. Add photo IDs to the queue")
    print("6. View queue")
    print("7. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == '1':  # Download only
        photo_id = get_photoid()
        with urlopen(f"{base}/gigapans/{photo_id}.kml") as response:
            photo_kml = response.read()
        dom = parseString(photo_kml)
        width = int(find_element_value(dom.documentElement, "maxWidth"))
        height = int(find_element_value(dom.documentElement, "maxHeight"))
        tile_size = int(find_element_value(dom.documentElement, "tileSize"))

        maxlevel = math.ceil(math.log(max(width, height) / tile_size, 2))
        wt, ht = math.ceil(width / tile_size) + 1, math.ceil(height / tile_size) + 1
        get_tiles(photo_id, base, maxlevel, wt, ht, tile_size)

    elif choice == '2':  # Assemble only
        photo_id = get_photoid()
        width = int(input("Enter image width: "))
        height = int(input("Enter image height: "))
        tile_size = int(input("Enter tile size: "))
        assemble_tiles(photo_id, width, height, tile_size)

    elif choice == '3':  # Download and assemble
        photo_id = get_photoid()
        with urlopen(f"{base}/gigapans/{photo_id}.kml") as response:
            photo_kml = response.read()
        dom = parseString(photo_kml)
        width = int(find_element_value(dom.documentElement, "maxWidth"))
        height = int(find_element_value(dom.documentElement, "maxHeight"))
        tile_size = int(find_element_value(dom.documentElement, "tileSize"))

        maxlevel = math.ceil(math.log(max(width, height) / tile_size, 2))
        wt, ht = math.ceil(width / tile_size) + 1, math.ceil(height / tile_size) + 1
        get_tiles(photo_id, base, maxlevel, wt, ht, tile_size)
        assemble_tiles(photo_id, width, height, tile_size)

    elif choice == '4':  # Process the queue
        while os.path.exists("queue.txt") and os.path.getsize("queue.txt") > 0:
            with open("queue.txt", "r") as queue:
                line = queue.readline().strip()
            if not line:
                break
            photo_id = int(line)
            logging.info(f"Processing photo ID: {photo_id}")
            with urlopen(f"{base}/gigapans/{photo_id}.kml") as response:
                photo_kml = response.read()
            dom = parseString(photo_kml)
            width = int(find_element_value(dom.documentElement, "maxWidth"))
            height = int(find_element_value(dom.documentElement, "maxHeight"))
            tile_size = int(find_element_value(dom.documentElement, "tileSize"))

            maxlevel = math.ceil(math.log(max(width, height) / tile_size, 2))
            wt, ht = math.ceil(width / tile_size) + 1, math.ceil(height / tile_size) + 1
            get_tiles(photo_id, base, maxlevel, wt, ht, tile_size)
            assemble_tiles(photo_id, width, height, tile_size)
            remove_first_line("queue.txt")

    elif choice == '5':  # Add to queue
        photo_ids = input("Enter photo IDs to add to queue (comma-separated): ").split(",")
        photo_ids = [int(photo_id.strip()) for photo_id in photo_ids if photo_id.strip().isdigit()]
        add_to_queue(photo_ids)
        time.time.sleep(2)

    elif choice == '6':  # View queue
        view_queue()

    elif choice == '7':  # Exit
        print("Exiting program. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 7.")
