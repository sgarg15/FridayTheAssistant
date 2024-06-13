def extractCode(text: str) -> str:
	"""
		This function is used to extract the code from the text.
	"""
	if '```python' not in text:
		return text
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