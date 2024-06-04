from libs.llm.chatbot import FridayLLM
from libs.utils.constants import Constants
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
        while True:
            content_in = input(self.colors.BOLD + "You: " + self.colors.END)
            if content_in:
                self.messages.append({'role': 'user', 'content': content_in})

            if content_in.lower() == "exit":
                break

            print(self.colors.BOLD + "\nAssistant: " + self.colors.END, end='')

            message = {'role': 'assistant', 'content': ''}
            async for response in self.fridayLLM.promptLLM(model, self.messages):
                content = response['message']['content']
                print(content, end='', flush=True)
                message['content'] += content

            self.messages.append(message)
            print("\n")
        print('Goodbye!')

    def runChat(self, model: str):
        asyncio.run(self.startChat(model=model))
