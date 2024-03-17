from PIL import Image
import os
import logging

def convert_jpeg_to_png(image_folder):
    logging.info("Starting conversion of JPEG to PNG...")

    # Counters for statistics
    converted_files = 0
    deleted_files = 0

    for image_file in os.listdir(image_folder):
        if image_file.endswith((".jpg", ".jpeg")):
            jpeg_path = os.path.join(image_folder, image_file)
            png_path = os.path.join(image_folder, os.path.splitext(image_file)[0] + '.png')
            
            # Log the conversion attempt
            logging.info(f"Converting {jpeg_path} to {png_path}...")
            with Image.open(jpeg_path) as img:
                img.save(png_path, "PNG")
            converted_files += 1
            
            # Log the deletion of the original file
            logging.info(f"Deleting original file {jpeg_path}...")
            os.remove(jpeg_path)
            deleted_files += 1
    
    # Summary log
    logging.info(f"Conversion completed. Total files converted: {converted_files}. Total files deleted: {deleted_files}.")