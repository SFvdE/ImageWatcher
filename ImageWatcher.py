import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

# Set your preferences here:
TARGET_FORMAT = "PNG"  # Change to "JPEG" or others if you want
DELETE_ORIGINAL = True  # Set to True if you want originals removed after conversion

def get_watch_folder(folder=None):
    if folder and os.path.isdir(folder):
        return folder
    else:
        # Default: Downloads folder
        return os.path.expanduser(r"~/Downloads")

class ImageConverterHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']:
            return

        print(f"New image detected: {filepath}")
        self.convert_image(filepath)

    def convert_image(self, filepath):
        tries = 5
        for attempt in range(tries):
            try:
                img = Image.open(filepath)
                base = os.path.splitext(filepath)[0]
                new_file = f"{base}.{TARGET_FORMAT.lower()}"

                if TARGET_FORMAT.upper() == 'JPEG':
                    img = img.convert('RGB')
                    img.save(new_file, TARGET_FORMAT, quality=95)
                else:
                    img.save(new_file, TARGET_FORMAT)

                print(f"Converted and saved to {new_file}")

                if filepath != new_file and DELETE_ORIGINAL:
                    os.remove(filepath)
                    print(f"Deleted original file {filepath}")

                break  # Success! Exit retry loop

            except FileNotFoundError:
                print(f"File not found yet, retrying ({attempt + 1}/5)...")
                time.sleep(0.5)
            except PermissionError:
                print(f"File is locked, retrying ({attempt + 1}/5)...")
                time.sleep(0.5)
            except Exception as e:
                print(f"Error converting image {filepath}: {e}")
                break  # Stop retrying on other errors

def batch_convert_existing(folder):
    print(f"Starting batch conversion in {folder}...")
    handler = ImageConverterHandler()
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']:
                if ext == f".{TARGET_FORMAT.lower()}":
                    print(f"Skipping {filename} (already in target format)")
                    continue
                print(f"Batch converting: {filename}")
                handler.convert_image(filepath)
    print("Batch conversion done.")

if __name__ == "__main__":
    # Change None to a string path to watch a custom folder, e.g. r"C:\MyImages"
    watch_folder = get_watch_folder(None)

    batch_convert_existing(watch_folder)

    event_handler = ImageConverterHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()
    print(f"Watching folder: {watch_folder} for new images...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

