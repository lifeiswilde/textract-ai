import pytesseract
from PIL import Image
import os
import logging
from multiprocessing import Pool
from utils import numeric_sort_key

def process_image(image_path: str, output_folder: str) -> None:
    """
    Process an image and extract text using pytesseract.
    
    Args:
        image_path (str): The path to the image file.
        output_folder (str): The path to the output folder.
    """
    try:
        with Image.open(image_path) as image:
            text = pytesseract.image_to_string(image)
        image_file = os.path.basename(image_path)
        output_file_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + '.txt')
        with open(output_file_path, 'w') as file:
            file.write(f"--- Page {image_file} ---\n{text}\n\n")
        logging.info(f"Successfully processed and extracted text from {image_file}.")
    except Exception as e:
        logging.error(f"Error processing {image_file}: {e}")

def extract_text_from_images(image_folder: str, output_folder: str) -> None:
    """
    Extract text from images in a folder using pytesseract.
    
    Args:
        image_folder (str): The path to the folder containing the images.
        output_folder (str): The path to the output folder.
    """
    logging.info("Starting text extraction from images...")
    os.makedirs(output_folder, exist_ok=True)
    image_files = [f for f in os.listdir(image_folder) if f.endswith((".jpg", ".jpeg", ".png"))]
    sorted_image_files = sorted(image_files, key=numeric_sort_key)
    if not sorted_image_files:
        logging.warning("No image files found in the specified folder.")
        return
    image_paths = [os.path.join(image_folder, image_file) for image_file in sorted_image_files]
    with Pool() as pool:
        pool.starmap(process_image, [(image_path, output_folder) for image_path in image_paths])
    logging.info(f"Completed text extraction from {len(sorted_image_files)} images.")