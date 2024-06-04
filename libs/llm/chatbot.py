import ollama

class FridayLLM:
    """
        This class is used to interact with the Ollama LLM. It contains functions that the FridayUI class uses to interact with the LLM.
    """
    def __init__(self):
        pass

    async def promptLLM(self, model: str, context: list):
        """
            This function is used to interact with the Ollama LLM. It takes in a model and a context and returns a response and uses yield to stream the response.
        """
        client = ollama.AsyncClient()
        async for response in await client.chat(model=model, messages=context, stream=True):
            yield response