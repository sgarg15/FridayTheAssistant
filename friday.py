import os

from libs.llm.fridayUI import FridayUI
import ollama
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from libs.memory.chromadb import FridayMemory



if __name__ == "__main__":
    friday = FridayUI()
    
    # mem = FridayMemory()
    
    # # ollamaEmbedder: OllamaEmbeddingFunction = OllamaEmbeddingFunction(url='http://localhost:11434/api/embeddings', model_name="nomic-embed-text", )
    # convo1 = [{'role': 'user', 'content': 'copy this file: C:\\Users\\satgarg\\Documents\\Resumes\\Satvik_Transcript_2024_2.pdf to my desktop', 'timestamp': 0}, {'role': 'assistant', 'content': "I'd be happy to help you with that! However, I need a bit more information from you. Since I'm a Python script, I don't have direct access to your file system or local files.\n\nTo clarify, I'll need to know the path of the file on your machine and the destination path where you want to copy it. In this case, you've mentioned that the source file is:\n\n`C:\\Users\\satgarg\\Documents\\Resumes\\Satvik_Transcript_2024_2.pdf`\n\nAnd you want to copy it to your desktop.\n\nCan you please confirm if the above information is correct?\n\nAlso, I'll need to know the operating system you're using (Windows, macOS, or Linux) and which Python version you have installed. This will help me provide a script that works correctly for you.\n\nOnce I get this information, I can generate a Python script to copy the file for you!", 'timestamp': 1}, {'role': 'user', 'content': 'yea copy it to my desktop. And I am using Windows. ', 'timestamp': 2}, {'role': 'assistant', 'content': 'I\'ll create a Python script to copy the file to your desktop. Here\'s the code:\n\n```\nimport os\nimport shutil\n\n# Define the source and destination paths\nsource_path = \'C:\\\\Users\\\\satgarg\\\\Documents\\\\Resumes\\\\Satvik_Transcript_2024_2.pdf\'\ndesktop_path = os.path.join(os.path.expanduser("~"), "Desktop")\n\n# Create the desktop path if it doesn\'t exist\nos.makedirs(desktop_path, exist_ok=True)\n\n# Define the destination file path\ndestination_path = os.path.join(desktop_path, \'Satvik_Transcript_2024_2.pdf\')\n\n# Copy the file\nshutil.copy(source_path, destination_path)\n```\n\nPlease note that you\'ll need to run this script in an environment where Python is installed and configured correctly. You can do this by saving the code as a `.py` file (e.g., `copy_file.py`) and then running it using Python:\n\n```\npython copy_file.py\n```\n\nMake sure to replace the source path with the correct location of your PDF file.\n\nOnce you run the script, the file should be copied to your desktop.', 'timestamp': 3}, {'role': 'user', 'content': 'exit', 'timestamp': 4}]
    
    # convo2 = [{'role': 'user', 'content': 'Can you create a file on my desktop', 'timestamp': 1718938835.898585}, {'role': 'assistant', 'content': "Before I can generate the Python script, could you please clarify some details?\n\n1. What should be the name of the file?\n2. What content should be written to the file (e.g., text, blank, or specific data)?\n3. Would you like me to create a new folder on your desktop if it doesn't exist already?\n\nPlease provide these clarifications, and I'll generate a Python script to accomplish your task!", 'timestamp': 1718938835.898585}, {'role': 'user', 'content': 'yea you can name it "bob" and it should be a tct document, and just make it directly on my desktop directory', 'timestamp': 1718938961.958759}, {'role': 'assistant', 'content': 'Here\'s the Python script to create a text file named "bob.txt" with no content on your desktop:\n\n```python\nimport os\n\n# Get the Desktop path\ndesktop_path = os.path.join(os.path.expanduser("~"), "Desktop")\n\n# Create the new file\nfile_path = os.path.join(desktop_path, \'bob.txt\')\n\n# Check if the file already exists and delete it if it does\nif os.path.exists(file_path):\n    os.remove(file_path)\n\n# Create a new text file with no content\nwith open(file_path, \'w\') as file:\n    pass\n\nprint(f"File \'{file_path}\' created on your desktop.")\n```\n\nPlease note that this script will overwrite any existing file named "bob.txt" on your desktop. If you want to avoid overwriting files, I can modify the script to prompt for confirmation before deleting an existing file.\n\nAlso, please ensure that you have write permissions in your desktop directory. If you encounter any issues, feel free to let me know!', 'timestamp': 1718938961.958759}, {'role': 'user', 'content': 'exit', 'timestamp': 1718946427.0866258}]


    
    
    # mem.store_conversation(convo)
    
    # mem.store_full_conversation(convo1)

    # print(mem.retrieve_relevant_conversations("copy a file to my desktop", 2))

    # print(ollamaEmbedder(convo))
    

    
    # textEmbedding = ollama.embeddings(model="nomic-embed-text", prompt='The sky is blue because of rayleigh scattering')
    # # print(textEmbedding)
    
    # client = chromadb.PersistentClient(path="./chromadb")

    # collection = client.get_or_create_collection(name="embeddings")
    
    # collection.upsert(
    #     documents=["Why sky"],
    #     embeddings=textEmbedding["embedding"],
    #     metadatas=[{"prompt": "The sky is blue because of rayleigh scattering"}],
    #     ids=["0"]
    # )
    
    # questionEmbed = ollama.embeddings(model="nomic-embed-text", prompt="What is the sky?")

    # results = collection.query(
    #     query_embeddings=questionEmbed["embedding"],
    #     n_results=2 # how many results to return
    # )
    
    # print(results)
   
    # friday.runChat(model="friday_codestral")
    friday.runChat(model="llama3-q8")
