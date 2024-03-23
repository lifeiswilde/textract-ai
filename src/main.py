import os
import logging
import constants
from pathlib import Path
from extract_text_from_images import extract_text_from_images
from convert_pdf_to_images import convert_pdf_to_images
from custom_openai_handler import create_client, process_text_with_openai
from convert_jpg_to_png import convert_jpeg_to_png
from argument_parse_handler import parse_arguments

logging.basicConfig(level=logging.INFO)

def main():
    args = parse_arguments()
    OPENAI_API_KEY = args.api_key
    OPENAI_PROMPT = args.prompt
    
    client = create_client(OPENAI_API_KEY)
    file_name = os.path.join("data", args.file)
    file_base_name = os.path.basename(file_name)
    job_id = os.path.splitext(file_base_name)[0]
    output_folder = os.path.join("output", "images_output", job_id)
    text_output_folder = os.path.join("output", "text_output", job_id)
    
    # Check if the job_id matches and the expected lengths are the same
    if not args.force and os.path.exists(output_folder) and os.path.exists(text_output_folder):
        num_images = len(os.listdir(output_folder))
        num_text_files = len(os.listdir(text_output_folder))
        if num_images == num_text_files:
            user_input = input(f"The job_id '{job_id}' already exists and the output lengths match. Do you want to replace the outputs? (y/n): ")
            if user_input.lower() != 'y':
                logging.info("User chose not to replace the outputs. Exiting.")
                return
    
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    Path(text_output_folder).mkdir(parents=True, exist_ok=True)
    num_pages = convert_pdf_to_images(file_name, output_folder=output_folder, batch_size=10)
    convert_jpeg_to_png(output_folder)
    extract_text_from_images(output_folder, text_output_folder)
    final_document_path = os.path.join(text_output_folder, 'final_processed_document.md')
    with open(final_document_path, 'w') as final_file:
        pass
    for text_file in sorted(os.listdir(text_output_folder)):
        if text_file.endswith(".txt"):
            text_file_path = os.path.join(text_output_folder, text_file)
            with open(text_file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            processed_text = process_text_with_openai(client, text_content, initial_prompt=OPENAI_PROMPT)
            with open(final_document_path, 'a', encoding='utf-8') as final_file:
                final_file.write(processed_text + '\n\n')
    logging.info("All pages have been processed and compiled into the final document.")

if __name__ == "__main__":
    main()
