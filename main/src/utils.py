import re
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

def numeric_sort_key(s: str) -> int:
    """
    Extract the numerical part of a string and return it as an integer.
    
    Args:
        s (str): The string to extract the numerical part from.
        
    Returns:
        int: The numerical part of the string as an integer.
    """
    return int(re.search(r'(\d+)', s).group(0))

def is_rate_limit_error(exception: Exception) -> bool:
    """
    Check if an exception is a rate limit error.
    
    Args:
        exception (Exception): The exception to check.
        
    Returns:
        bool: True if the exception is a rate limit error, False otherwise.
    """
    return "Rate limit" in str(exception)

def retry_decorator(func):
    """
    Decorator to retry a function if a rate limit error occurs.
    
    Args:
        func (function): The function to decorate.
        
    Returns:
        function: The decorated function.
    """
    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=60),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(is_rate_limit_error)
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper