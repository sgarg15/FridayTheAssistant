import sys
from time import sleep

import re

def extractCode(text: str) -> list:
    """
    This function is used to extract the code from the text. There might be more than one code block in the text.
    This function will extract all the code blocks and return a list of code blocks.
    """
    code_blocks = []
    delimiter = '```'
    
    while delimiter in text:
        # Find the start of the first code block
        start = text.find(delimiter)
        if start == -1:
            break
        # Adjust start to be after the initial delimiter
        start += len(delimiter)
        
        # Find the end of the code block
        end = text.find(delimiter, start)
        if end == -1:
            break
        
        # Extract the code block
        code_block = text[start:end].strip()
        
        # If the code block starts with a language specifier, remove it
        if '\n' in code_block:
            first_line, rest = code_block.split('\n', 1)
            if first_line.strip().isalpha():
                code_block = rest.strip()
        
        code_blocks.append(code_block)
        
        # Move the text index past the end of the current code block
        text = text[end + len(delimiter):]
    
    return code_blocks
def extractContent(text: str) -> list:
    """
        This function is used to extract the content from the text. There might be more than one content block in the text. This function will extract all the content blocks and return a list of content blocks.
    """
    if '```python' not in text:
        return text
    
    return re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    
def typeEffect(text: str, delay=0.5) -> str:
    """
    Prints the given text one character at a time with a delay between each character.
    
    Parameters:
    text (str): The text to be printed.
    delay (float): The delay between each character in seconds. Default is 0.5 seconds.
    """
    for char in text:
        sleep(delay)
        sys.stdout.write(char)
        sys.stdout.flush()
