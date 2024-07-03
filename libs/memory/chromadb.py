import ollama
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
import math
from libs.llm.chatbot import FridayLLM
from libs.utils.logging.logger import logger
import datetime

class FridayMemory:
    def __init__(self):
        self.memoryClient = chromadb.PersistentClient(path="./chromadb")
        self.analyzer = FridayLLM()
        self.ollamaEmbedder = OllamaEmbeddingFunction(url='http://localhost:11434/api/embeddings', model_name="nomic-embed-text")
        self.conversationsDB = self.memoryClient.get_or_create_collection('friday_conversations', metadata={"hnsw:space": 'cosine'}) #This is cosine distance NOT similarity. similarity is 1 - cosine distance. So if cosine distance is 0 that means the two vectors are the same.
        
    async def process_user_msg_with_memory(self, user_msg: str) -> str:
        """
        Process the user message with memory by retrieving relevant information from memory based on the input query.
        
        Parameters:
            user_msg (str): The user message to process.
        
        Returns:
            str: The processed context query after memory retrieval and potential addition of relevant information.
        """
        
        context_query = user_msg
        
        numOfMemories = self.conversationsDB.count()
        
        ## First do memory retrieval and add to the context_query
        if numOfMemories > 0:
            context_query = await self._memory_retrieval(context_query)
  
  
        ## Check to see if any infromation is needed to put in memory
        await self._memory_storage(context_query)
        
        return context_query
        
    async def _analyze_query(self, query: str, prompt: str) -> str:
        """
        Analyze a query using a specified model and prompt.

        Args:
            query (str): The query to analyze.
            prompt (str): The prompt to use for analysis.

        Returns:
            str: The content of the response message.

        This function logs an "ANALYZING QUERY" message using the logger. It then sets the model to "phi3:3.8b-mini-128k-instruct-q8_0" and calls the analyzerLLm method of the analyzer object with the specified model, query, and prompt. The response from the analyzer is returned as the content of the response message.
        """
        
        logger.info("ANALYZING QUERY")
        model = "phi3:3.8b-mini-128k-instruct-q8_0"
        
        response = await self.analyzer.analyzerLLm(model, query, prompt)
        
        return response['response']
        
    async def _memory_retrieval(self, query: str, k=5) -> str:
        """
        Retrieves relevant information from memory based on the input query.
        
        Parameters:
            query (str): The query used to search for relevant information.
            k (int): The number of relevant memories to retrieve, default is 5.
        
        Returns:
            str: The retrieved relevant information from memory.
        """
        logger.info("LOOKING FOR RELEVANT INFO IN MEMORY")
        
        # Use the query directly to get the relevant information from the memory
        memories_list = self._retrieve_relevant_memories(query)
        
        # Using Phi3 check if there is a Task in the query. Have it only return Yes or No. And the prompt can be:
            # "Does any part of the TEXT ask the agent to perform a task or solve a problem? Answer with just one word, yes or no."
        containsTask = await self._analyze_query(query, "Does any part of the TEXT ask the agent to perform a task or solve a problem? Answer with just one word, yes or no.")
        
        # IF YES:
        if "yes" in containsTask.lower():
            # Again using phi3 mdoel, extract the task from the text and return it. And the prompt can be:
            task = await self._analyze_query(query, "Copy just the task from the TEXT, then stop. Don't solve it, and don't include any advice.")
                
            # Generalize the task given from the previous step. And the prompt can be:
            generalizedTask = await self._analyze_query(task, "Summarize very briefly, in general terms, the type of task described in the TEXT. Leave out details that might not appear in a similar problem.")       
            
            # Query to memory using the generalized task
            memories_list.extend(self._retrieve_relevant_memories(generalizedTask))
        
        # Remove any duplicates from the returned memories, ie. if the same memory is returned twice it will only be returned once in the list of memories
        memories_list = list(set(memories_list))
                        
        logger.info(f"RELEVANT INFO IN MEMORY: {memories_list}")
        
        # Add the new memories to the query
        return query + self._memories_to_string(memories_list)

    ## UPDATE TO NOT ADD MEMORY IF IT ALREADY EXISTS
    async def _memory_storage(self, query:str):
        """
        Asynchronously stores relevant information from a given query in memory.

        Parameters:
            query (str): The query to process.

        Returns:
            None

        This function checks if the query contains a task by analyzing the query using the `_analyze_query` method.
        If a task is found, it extracts advice from the query and stores it in memory if it exists.
        Then, it extracts the task from the query, generalizes it, and stores the task/advice pair in memory.

        After that, it checks if the query contains information that can be stored in memory.
        If it does, it extracts the question and answer from the query and stores them in memory.
        """
        # Check to see if the query contains a task. The prompt can be:
            # Does any part of the TEXT ask the agent to perform a task or solve a problem? Answer with just one word, yes or no.
        containsTask = await self._analyze_query(query, "Does any part of the TEXT ask the agent to perform a task or solve a problem? Answer with just one word, yes or no.")
        
        # if YES:
        if "yes" in containsTask.lower():
            # Extract any advice from the query that can be used for future queries. And the prompt can be:
                # "Briefly copy any advice from the TEXT that may be useful for a similar but different task in the future. But if no advice is present, just respond with 'none'."
            advice = await self._analyze_query(query, "Briefly copy any advice from the TEXT that may be useful for a similar but different task in the future. But if no advice is present, just respond with 'none'.")
            
            # If YES ADVICE:
            if "none" not in advice.lower():
                # Extract the task from the query
                    # "Briefly copy just the task from the TEXT, then stop. Don't solve it, and don't include any advice.""
                task = await self._analyze_query(query, "Copy just the task from the TEXT, then stop. Don't solve it, and don't include any advice.")
                
                # Generalize the task given from the previous step
                    # "Summarize very briefly, in general terms, the type of task described in the TEXT. Leave out details that might not appear in a similar problem."
                generalizedTask = await self._analyze_query(task, "Summarize very briefly, in general terms, the type of task described in the TEXT. Leave out details that might not appear in a similar problem.")
                
                # Store the task/advice pair in the memory
                self._store_pair_in_memory(generalizedTask, advice)
                
                logger.info(f"Following Memory Pair Stored: \n{generalizedTask} : {advice}")
                    
        
        # Check to see if query has information that can should be committed to memory. And the prompt can be:
            # "Does the TEXT contain information that could be committed to memory? Answer with just one word, yes or no."
        containsInfo = await self._analyze_query(query, "Does the TEXT contain information that could be committed to memory? Answer with just one word, yes or no.")
        
        # If YES:
        if "yes" in containsInfo.lower():
            # What would the question be like to retrieve this memory? And the prompt can be:
                # "Imagine that the user forgot this information in the TEXT. How would they ask you for this information? Include no other text in your response."
            question = await self._analyze_query(query, "Imagine that the user forgot this information in the TEXT. How would they ask you for this information? Include no other text in your response.")
            
            # Extract any information that should be stored in memory. And the prompt can be:
                # "Copy the information from the TEXT that should be committed to memory. Add no explanation."
            answer = await self._analyze_query(query, "Copy the information from the TEXT that should be committed to memory. Add no explanation.")
            
            # Store the Question/Answer Pair in the memory
            self._store_pair_in_memory(question, answer)
            
            logger.info(f"Following Memory Pair Stored: \n{question} : {answer}")
          
    def _store_pair_in_memory(self, item1, item2):
        """
        Store a pair of item1 and item2 in the memory.

        Parameters:
            item1 (any): The query/document to be stored.
            item2 (any): The metadata associated with the query/document.

        Returns:
            None: This function does not return anything.
        """
        
        item1_embedding = self.ollamaEmbedder(item1)
        
        self.conversationsDB.upsert(ids=[str(datetime.datetime.now())], documents=item1, embeddings=item1_embedding[0], metadatas=[{"response": item2, "timestamp": str(datetime.datetime.now())}])
        
        return
        
    def _retrieve_relevant_memories(self, query: str, k=5, threshold=0.4):
        """
        Retrieves relevant memories based on a given query.

        Args:
            query (str): The query to search for relevant memories.
            k (int, optional): The number of results to retrieve. Defaults to 5.
            threshold (float, optional): The distance threshold for considering a memory relevant. Defaults to 0.4.

        Returns:
            list: A list of tuples containing the document, metadata, and distance of the retrieved memories.

        This function generates an embedding for the given query using the `ollamaEmbedder` method. It then queries the `conversationsDB` for relevant conversations based on the query embedding. The function iterates through the results and adds them to the `memories` list if the distance is less than the threshold. The function returns the `memories` list.
        """
        # Generate embedding for the query
        query_embedding = self.ollamaEmbedder(query)
        
        memories = []
        
        # Retrieve relevant conversations based on the query embedding
        results = self.conversationsDB.query(
            query_embeddings=query_embedding[0],
            n_results=k,
        )

        number_of_results = len(results['distances'][0])
        
        # Iterate through the results and add them to the memos list if the distance is less than the threshold
        for i in range(number_of_results):
            id, document, distance, metadata = results['ids'][0][i], results['documents'][0][i], results['distances'][0][i], results['metadatas'][0][i]['response']
            
            if math.isclose(distance, 0, abs_tol=1e-8):
                results['distances'][0][i] = 0.0
                
            if distance < threshold:
                logger.debug("\nINPUT-OUTPUT PAIR RETRIEVED FROM VECTOR DATABASE:\n  INPUT1\n    {}\n  OUTPUT\n    {}\n  DISTANCE\n    {}".format(document, metadata, distance))
                memories.append((document, metadata, distance))
                
        memories_text_list = [memory[1] for memory in memories]
        
        return memories_text_list
    
    def _memories_to_string(self, memories: list) -> str:
        """
        Converts a list of memories into a formatted string.
        :param memories: A list of memories to be converted.
        :return: A string representing the memories with specific formatting.
        """
        memories_text = ""
        
        if len(memories) > 0:
            info = "\n # Memories that might help to complete the task \n"
            for memories in memories:
                info = info + "- " + memories + "\n"
            memories_text = memories_text + "\n" + info
            
        return memories_text
    
    #-----------------------
    
    def augment_query_with_context(self, query):
        relevant_conversations = self.retrieve_relevant_conversations(query, 2)
        if len(relevant_conversations['metadatas']) == 0:
            return query
        metadata = relevant_conversations['metadatas'][0]
        context = metadata[0]['assistantReply']
        augmented_query = f"Context:\n{context}\n\nQuery:\n{query}"
        return augmented_query
    
    def clean_conversation(self):
        self.conversationsDB.delete()
        
    def get_all_items(self):
        results = self.conversationsDB.get()
        return results
    
    def store_conversation_per_interaction(self, interaction: list):
        # Idea is to store every interaction between the user and the assistant. So the document will be the users message and the metadata will contain the timestamp and the message returned by the assistant. 
        # The interaction will be a list of 2 messages. The first message will be the user message and the second message will be the assistant message. Each message will have a role and a timestamp and content.
        
        # Generate embedding for each message in the conversation
        try:
            #Where the role is user get that content from the interaction
            userContent = "\n".join([message['content'] for message in interaction if message['role'] == 'user'])
            assistantContent = "\n".join([message['content'] for message in interaction if message['role'] == 'assistant'])
            userEmbedding = self.ollamaEmbedder(userContent)
            
            self.conversationsDB.upsert(
                documents=[userContent],
                embeddings=userEmbedding[0],
                metadatas=[{"assistantReply": assistantContent, "timestamp": interaction[0]['timestamp']}],
                ids=[str(interaction[0]['timestamp'])]
            )
            logger.info(f"Stored interaction")
        except Exception as e:
            logger.error(f"Error storing interaction: {e}")
        
    def store_conversation_per_message(self, conversation):
        # Generate embedding for each message in the conversation
        embeddings = []
        
        for message in conversation:
            messageEmbedding = self.ollamaEmbedder(message['content'])
            embeddings.append(messageEmbedding[0])
            
        
        messages = [str(message['content'].strip()) for message in conversation]
            
        # Store the conversation along with its embedding
        self.conversationsDB.upsert(
            documents=messages,
            embeddings=embeddings,
            metadatas=[{"role": message['role'], "timestamp": message['timestamp']} for message in conversation],
            ids=[str(message['timestamp']) for message in conversation]
        )
        
        logger.info(f"Stored conversation")
        
    def store_full_conversation(self, conversation):
        #Join the conversation into a single string
        messages = "\n".join([message['content'] for message in conversation])
        
        entireConversationEmbedding = self.ollamaEmbedder(messages)
        
        # Store the conversation along with its embedding
        self.conversationsDB.add(
            documents=messages,
            embeddings=entireConversationEmbedding[0],
            metadatas=[{"role": conversation[0]['role'], "timestamp": conversation[0]['timestamp']}],
            ids=[str(conversation[0]['timestamp'])]
        )
        
        logger.info(f"Stored conversation")
                