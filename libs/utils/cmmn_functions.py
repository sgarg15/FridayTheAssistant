import sys
from time import sleep

def extractCode(text: str) -> str:
    """
        This function is used to extract the code from the text.
    """
    if '```python' not in text:
        return ""
    return text.split('```python')[1].split('```')[0]

def extractContent(text: str) -> str:
    """
        This function is used to extract the content from the text.
    """
    if '```python' not in text:
        return text
    
    beforeCode = text.split('```python')[0]
    afterCode = text.split('```python')[1].split('```')[1]
    
    return beforeCode + "\n[code]\n" + afterCode
    # return beforeCode + "\n" + afterCode

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
