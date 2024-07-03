import ollama
from libs.utils.logging.logger import logger

class FridayLLM:
    """
        This class is used to interact with the Ollama LLM. It contains functions that the FridayUI class uses to interact with the LLM.
    """
    def __init__(self):
        self.client: ollama.AsyncClient = ollama.AsyncClient()


    async def promptLLM(self, model: str, context: list):
        """
            This function is used to interact with the Ollama LLM. It takes in a model and a context and returns a response and uses yield to stream the response.
        """
        
        try:
            async for response in await self.client.chat(model=model, messages=context, stream=True):
                yield response
        except Exception as e:
            # Handle the exception here
            logger.error(f"Error: {e}")
            
    async def analyzerLLm(self, model: str, query: str, prompt: str) -> str:
        """
            This function is used to interact with the Ollama LLM. It takes in a model and a context and returns a response and uses yield to stream the response.
        """
        
        text_analyze = "# TEXT \n" + query + "\n"
        
        analysis_prompt = "# INSTRUCTIONS\n" + prompt + "\n"
        
        user_msg_with_prompt = "\n".join([analysis_prompt, text_analyze])
        
        print(user_msg_with_prompt)
               
        try:
            return await self.client.generate(model=model, prompt=user_msg_with_prompt)
        except Exception as e:
            # Handle the exception here
            logger.error(f"Error: {e}")