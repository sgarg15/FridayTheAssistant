<a name="readme-top"></a>

[![LinkedIn][linkedin-shield]][linkedin-url]
[![Twitter][twitter-shield]][twitter-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">Friday The Assistant</h1>

  <p align="center">
    Summer of Shipping project! An AI assistant that has full control over your computer and its applications!  
    <br />

  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

Imagine a local AI assistant that can do anything you want. Anything that you can do on a computer, it can do. And the best part... it runs fully locally! So no worries about your data being sent to a server hidden away in the depths of the internet. 

Using Ollama and its ability to runs Large Language Models locally, this project will allow a user to interact with their computer using natural language. For instance, you can ask it to open a file, run a program, or even write a document for you. The possibilities are endless! 

I plan on using `Llama3` for the chat functionality of the assistant and `Codestral` for the code creation/executing functionality. Both of which are listed here: [Ollama](https://ollama.com/library)

## MindMapping

![image](https://github.com/sgarg15/FridayTheAssistant/assets/47345135/fe8cf64b-4d83-4a69-8f69-a9571dc9a5ce)

Currently researching effective ways to do "Dependency & Security Checks" on the Python code generated by Codestral... Its proving quite difficult :(. 

### Built With

* [![Ollama][ollama.com]][Ollama-url]
* [![Python][python.org]][Python-url]

## Getting Started
In the systems current state, it is quite easy to get started. Just clone the repository using the following command:

### Prerequisites
* Python 3.11 or higher
* Ollama Installed on Linux System [Ollama Installation](https://ollama.com/download/linux)
* Codestral/Llama3 Installed on Linux System [Model Installation](https://ollama.com/library)
* Ollama running through the command line, with the following command: `ollama serve`

And you should be good to go! (Post an issue if something goes wrong!)

### Installation

```sh
git clone https://github.com/sgarg15/FridayTheAssistant
```

Then, navigate to the directory and run the following command to install the required dependencies:
```sh
pip install -r requirements.txt
```

Finally, run the following command to start the assistant:
```sh
python3 friday.py
```

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/satvikgarg15/
[twitter-shield]: https://img.shields.io/badge/Twitter-00000?style=for-the-badge&logo=x&colorB=555
[twitter-url]: https://twitter.com/sgarg0310

[python.org]: https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=white
[ollama.com]: https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white
[Ollama-url]: https://ollama.com/
[Python-url]: https://www.python.org/
