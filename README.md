# TextractAI

TextractAI is a Python-based project that extracts text from PDF files, processes the extracted text using the OpenAI API, and generates a final processed document. The project utilizes various libraries and tools to perform PDF-to-image conversion, image-to-text extraction, and text processing.

## Why TextractAI?

Despite advancements in OCR technology, achieving perfect accuracy remains a challenge. The quality of the extracted text often depends on factors such as image resolution, font variations, layout complexities, and noise in the document.

TextractAI aims to address these limitations and enhance the accuracy of text recognition from documents. By leveraging a combination of OCR techniques and LLMs (OpenAI), TextractAI goes beyond traditional OCR approaches to deliver more reliable and precise text extraction results.

## Features

- Converts PDF files to images using `pdf2image`
- Extracts text from images using `pytesseract`
- Processes the extracted text using the OpenAI API
- Handles rate limiting and retries for the OpenAI API calls
- Supports parallel processing for faster execution
- Allows customization of the OpenAI prompt and API key
- Provides a command-line interface for easy usage

## Prerequisites

- Python 3.6 or higher
- OpenAI API key
- Tesseract OCR (required by `pytesseract`)

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/your-username/textractai.git
  ```
2. Change to the project directory:
  ```bash
  cd textractai
  ```
3. Create a virtual environment:
  ```bash
  python3 -m venv venv
  ```
4. Activate the virtual environment:
  ```bash
  source venv/bin/activate
  ```
5. Install required dependencies:
  ```bash
  pip install -r requirements.txt
  ```
6. Set up the OpenAI API key:
    - Either set the `OPENAI_API_KEY` environment variable with your API key, or
    - Provide the API key using the `--api-key` or `-k` command-line argument when running the script

## Usage

To run the TextractAI script, use the following command:
```bash
python src/main.py --file <path_to_pdf_file> [--output <output_folder>] [--text-output <text_output_folder>] [--api-key <openai_api_key>] [--prompt <custom_prompt>] [--force]
```

Options:
- `--file` or `-f`: Path to the PDF file to process (required)
- `--output` or `-o`: Path to the output folder for generated images (default: ./output/images_output)
- `--text-output` or `-t`: Path to the output folder for extracted text files (default: ./output/text_output)
- `--api-key` or `-k`: OpenAI API key (required if `OPENAI_API_KEY` environment variable is not set)
- `--prompt` or `-p`: Custom OpenAI prompt (optional, default prompt will be used if not provided)
- `--force`: Force overwrite of existing outputs without prompting

## Example Usage
```bash
python src/main.py --file data/example.pdf --output output/images --text-output output/text --api-key your_api_key --prompt "Custom prompt for processing the text"
```

## Project Structure

- `data/`: Directory to store input PDF files
- `output/`: Directory to store output files
  - `images_output/`: Generated images from PDF conversion
  - `text_output/`: Extracted text files from images
- `src/`: Source code directory
  - `main.py`: Main script to run the TextractAI pipeline
  - `argument_parse_handler.py`: Handles command-line argument parsing
  - `constants.py`: Contains constant values used across the project
  - `convert_jpg_to_png.py`: Converts JPEG images to PNG format
  - `convert_pdf_to_images.py`: Converts PDF files to images
  - `custom_openai_handler.py`: Handles OpenAI API calls and processing
  - `extract_text_from_images.py`: Extracts text from images using OCR
  - `utils.py`: Utility functions used in the project
- `requirements.txt`: Lists the required Python dependencies

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
