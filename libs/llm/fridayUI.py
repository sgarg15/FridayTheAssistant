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
        self.memoryModule = FridayMemory()
        self.constants = Constants()
        self.colors = self.constants.color
        self.runner = Runner()
        self.messages = []
      
    async def startChat(self, model: str):
        while True:
            content_in = input(self.colors.BOLD + "You: " + self.colors.END)
            logger.info(f"Context Query: \n{content_in}")
            user_msg = {'role': 'user', 'content': content_in, 'timestamp': time.time()}
            current_interaction = [user_msg]
            if content_in.lower() == "exit":
                break

            # Memory things start here before sending to the LLM
            msg_with_context = await self.memoryModule.process_user_msg_with_memory(user_msg)

            if content_in:
                self.messages.append(msg_with_context)
            else:
                continue
            
            print(self.colors.BOLD + "\nAssistant: " + self.colors.END, end='')

            assistant_msg = {'role': 'assistant', 'content': '', 'timestamp': time.time()}
            async for response in self.fridayLLM.promptLLM(model, self.messages):
                content = response['message']['content']
                #Print the assistant's response
                print(content, end='', flush=True)
                assistant_msg['content'] += content
                
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