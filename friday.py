import os

from libs.llm.fridayUI import FridayUI

if __name__ == "__main__":
    friday = FridayUI()
    # friday.runChat(model="friday_codestral")
    friday.runChat(model="friday_llama")
   
