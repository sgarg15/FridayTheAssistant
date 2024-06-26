import time
import ollama
from libs.llm.chatbot import FridayLLM
from libs.memory.chromadb import FridayMemory
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
        self.client: ollama.AsyncClient = ollama.AsyncClient()
        self.memoryModule = FridayMemory()
        self.constants = Constants()
        self.colors = self.constants.color
        self.runner = Runner()
        self.messages = []

    async def startChat(self, model: str):
        while True:
            content_in = input(self.colors.BOLD + "You: " + self.colors.END)
            conextQuery = self.memoryModule.augment_query_with_context(content_in)
            logger.info(f"Context Query: \n{conextQuery}")
            user_msg = {'role': 'user', 'content': conextQuery, 'timestamp': time.time()}
            current_interaction = [user_msg]
            
            if content_in:
                self.messages.append(user_msg)
            else:
                continue

            if content_in.lower() == "exit":
                break

            print(self.colors.BOLD + "\nAssistant: " + self.colors.END, end='')

            assistant_msg = {'role': 'assistant', 'content': '', 'timestamp': time.time()}
            async for response in self.fridayLLM.promptLLM(model, self.messages, self.client):
                content = response['message']['content']
                #Print the assistant's response
                print(content, end='', flush=True)
                assistant_msg['content'] += content
                
            current_interaction.append(assistant_msg)
            self.memoryModule.store_conversation_per_interaction(current_interaction)
            self.messages.append(assistant_msg)
                        
            #Format the response to get the code and get any content before or after the code
            msg_content: str = assistant_msg['content']
            
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
        # logger.info(f"conversation: \n{self.messages}")
        print('Goodbye!')

    def runChat(self, model: str):
        asyncio.run(self.startChat(model=model)) 