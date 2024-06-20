import ollama
from libs.llm.chatbot import FridayLLM
from libs.utils.cmmn_functions import extractCode, extractContent, typeEffect
from libs.utils.constants import Constants
from libs.utils.logging.logger import logger
import asyncio

from libs.utils.terminal.runner import Runner

class FridayUI:
    """
        This class will be used by the "frontend" to interact with the LLM.
    """
    def __init__(self):
        self.fridayLLM = FridayLLM()
        self.constants = Constants()
        self.colors = self.constants.color
        self.runner = Runner()
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
            
            # typeEffect(llmContent, delay=0.01)
            
            # if llmCode:
            #     # Ask the user if they want to execute the code
            #     print("\n\n")
            #     typeEffect(llmCode, delay=0.01)
                
            #     user_input = input("\n\nDo you want to execute the code above? (y/n): ")
                
            #     if user_input.lower() == 'y':
            #         # Execute the code
            #         consoleOutput = self.runner.runCode(llmCode)
            #         logger.info(f"Console Output: \n{consoleOutput}")
            #     else:
            #         print("Code not executed.")        

            print("\n")
        print('Goodbye!')

    def runChat(self, model: str):
        asyncio.run(self.startChat(model=model)) 