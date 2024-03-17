import logging
from openai import OpenAI
from constants import OPENAI_PROMPT
from multiprocessing import Pool, Manager
from typing import List, Dict
from utils import retry_decorator

logging.basicConfig(level=logging.INFO)

def create_client(api_key: str) -> OpenAI:
    """
    Create an OpenAI client instance.
    
    Args:
        api_key (str): The OpenAI API key.
        
    Returns:
        OpenAI: An OpenAI client instance.
    """
    logging.info("Creating OpenAI client...")
    client = OpenAI(api_key=api_key)
    logging.info("OpenAI client created successfully.")
    return client

@retry_decorator
def chat_completion(client: OpenAI, messages: List[Dict[str, str]], model: str = "gpt-4-1106-preview") -> Dict:
    """
    Request a chat completion from the OpenAI API.
    
    Args:
        client (OpenAI): An OpenAI client instance.
        messages (List[Dict[str, str]]): A list of message dictionaries, each containing a role and content.
        model (str, optional): The OpenAI model to use. Defaults to "gpt-4-1106-preview".
        
    Returns:
        Dict: The response from the OpenAI API.
    """
    logging.info(f"Requesting chat completion with model {model}...")
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    logging.info("Chat completion request successful.")
    return response

def process_text(args: tuple) -> str:
    """
    Process text using the OpenAI API.
    
    Args:
        args (tuple): A tuple containing the OpenAI client, text, model, initial prompt, and result queue.
        
    Returns:
        str: The processed text.
    """
    client, text, model, initial_prompt, result_queue = args
    processed_text = process_text_with_openai(client, text, model, initial_prompt)
    result_queue.put(processed_text)

def process_text_with_openai(client: OpenAI, text: str, model: str = "gpt-4", initial_prompt: str = OPENAI_PROMPT) -> str:
    """
    Process text using the OpenAI API.
    
    Args:
        client (OpenAI): An OpenAI client instance.
        text (str): The text to process.
        model (str, optional): The OpenAI model to use. Defaults to "gpt-4".
        initial_prompt (str, optional): The initial prompt for the OpenAI API. Defaults to OPENAI_PROMPT.
        
    Returns:
        str: The processed text.
    """
    logging.info("Processing text with OpenAI...")
    messages = [
        {
            "role": "system",
            "content": initial_prompt,
        },
        {
            "role": "user",
            "content": text,
        }
    ]
    response = chat_completion(client, messages, model=model)
    if response:
        processed_text = response.choices[0].message.content
        preview_text = (processed_text[:75] + '...') if len(processed_text) > 75 else processed_text
        logging.info(f"Text processed successfully. Preview: {preview_text}")
        return processed_text
    else:
        logging.info("No response from OpenAI.")
        return "Error processing text with OpenAI."

def process_texts_in_parallel(client: OpenAI, texts: List[str], model: str = "gpt-4", initial_prompt: str = OPENAI_PROMPT) -> List[str]:
    """
    Process multiple texts in parallel using the OpenAI API.
    
    Args:
        client (OpenAI): An OpenAI client instance.
        texts (List[str]): A list of texts to process.
        model (str, optional): The OpenAI model to use. Defaults to "gpt-4".
        initial_prompt (str, optional): The initial prompt for the OpenAI API. Defaults to OPENAI_PROMPT.
        
    Returns:
        List[str]: A list of processed texts.
    """
    with Manager() as manager:
        result_queue = manager.Queue()
        with Pool() as pool:
            pool.map(process_text, [(client, text, model, initial_prompt, result_queue) for text in texts])
        processed_texts = []
        while not result_queue.empty():
            processed_texts.append(result_queue.get())
    return processed_texts