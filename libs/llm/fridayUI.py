import ollama
from libs.llm.chatbot import FridayLLM
from libs.utils.cmmn_functions import extractCode, extractContent
from libs.utils.constants import Constants
from libs.utils.logging.logger import logger
import asyncio

class FridayUI:
    """
        This class will be used by the "frontend" to interact with the LLM.
    """
    def __init__(self):
        self.fridayLLM = FridayLLM()
        self.constants = Constants()
        self.colors = self.constants.color
        self.messages = []

    async def startChat(self, model: str):
        client: ollama.AsyncClient = ollama.AsyncClient()
        
        while True:
            content_in = input(self.colors.BOLD + "You: " + self.colors.END)
            if content_in:
                self.messages.append({'role': 'user', 'content': content_in})

            if content_in.lower() == "exit":
                break

            print(self.colors.BOLD + "\nAssistant: " + self.colors.END, end='')

            message = {'role': 'assistant', 'content': ''}
            async for response in self.fridayLLM.promptLLM(model, self.messages, client):
                content = response['message']['content']
                print(content, end='', flush=True)
                message['content'] += content

            self.messages.append(message)
            
            #Format the response to get the code and get any content before or after the code
            msg_content: str = message['content']
            
            llmCode = extractCode(msg_content)
            logger.info(f"Code: \n{llmCode}")
            
            llmContent = extractContent(msg_content)
            logger.info(f"Content: \n{llmContent}")

            print("\n")
        print('Goodbye!')

    def runChat(self, model: str):
        asyncio.run(self.startChat(model=model))
