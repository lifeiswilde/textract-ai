import logging
import pdfplumber
from pdf2image import convert_from_path
from pathlib import Path
from multiprocessing import Pool


def convert_batch(args):
    pdf_path, output_folder, dpi, start_page, end_page = args
    images = convert_from_path(pdf_path, dpi=dpi, first_page=start_page+1, last_page=end_page, thread_count=4)
    for j, image in enumerate(images, start=start_page):
        image_path = f"{output_folder}/page_{j+1}.png"
        try:
            image.save(image_path, 'PNG')
            logging.info(f"Successfully saved {image_path}")
        except Exception as e:
            logging.error(f"Failed to save image {image_path}: {e}")
    del images

def convert_pdf_to_images(pdf_path, output_folder, dpi=600, batch_size=10):
    logging.info(f"Starting conversion of PDF to images with DPI={dpi}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            logging.info(f"We found a total of {num_pages} pages to process...")
            
            batches = [(pdf_path, output_folder, dpi, i, min(i + batch_size, num_pages)) for i in range(0, num_pages, batch_size)]
            with Pool() as pool:
                pool.map(convert_batch, batches)
    except Exception as e:
        logging.error(f"Failed to convert PDF to images: {e}")
        return 0
    return num_pages