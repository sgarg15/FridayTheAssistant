import ollama
from libs.utils.logging.logger import logger

class FridayLLM:
    """
        This class is used to interact with the Ollama LLM. It contains functions that the FridayUI class uses to interact with the LLM.
    """
    def __init__(self):
        pass

    async def promptLLM(self, model: str, context: list, client: ollama.AsyncClient):
        """
            This function is used to interact with the Ollama LLM. It takes in a model and a context and returns a response and uses yield to stream the response.
        """
        
        try:
            async for response in await client.chat(model=model, messages=context, stream=True):
                yield response
        except Exception as e:
            # Handle the exception here
            logger.error(f"Error: {e}")