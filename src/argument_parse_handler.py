import argparse
import constants
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process PDF and extract text using OpenAI.")
    parser.add_argument("-f", "--file", required=True, help="Path to the PDF file")
    parser.add_argument("-o", "--output", default="./output_folder", help="Path to the output folder (default: ./output_folder)")
    parser.add_argument("-t", "--text-output", default="./text_output_folder", help="Path to the text output folder (default: ./text_output_folder)")
    
    api_key_env = os.environ.get('OPENAI_API_KEY')
    parser.add_argument("-k", "--api-key", required=not api_key_env, help="OpenAI API key (required if OPENAI_API_KEY environment variable is not set)")
    parser.add_argument("-p", "--prompt", default=constants.OPENAI_PROMPT, help="OpenAI prompt (optional, will use the default from constants if not provided)")
    parser.add_argument("--force", action="store_true", help="Force overwrite of existing outputs without prompting")
    args = parser.parse_args()
    return args