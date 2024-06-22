import ollama
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from libs.utils.logging.logger import logger

class FridayMemory:
    def __init__(self):
        self.memoryClient = chromadb.PersistentClient(path="./chromadb")
        self.ollamaEmbedder = OllamaEmbeddingFunction(url='http://localhost:11434/api/embeddings', model_name="nomic-embed-text")
        self.conversationsDB = self.memoryClient.get_or_create_collection('friday_conversations', embedding_function=self.ollamaEmbedder, metadata={"hnsw:space": "cosine"})
        
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
                
    def retrieve_relevant_conversations(self, query: str, k=5):
        # Generate embedding for the query
        query_embedding = self.ollamaEmbedder(query)
        # Retrieve relevant conversations based on the query embedding
        results = self.conversationsDB.query(
            query_embeddings=query_embedding[0],
            n_results=k,
            where={
                "$or": [
                    {
                        "role": {
                            "$eq": "assistant"
                        }
                    },
                    {
                        "role": {
                            "$eq": "user"
                        }
                    }
                ]
            }
        )
        return results
    
    def augment_query_with_context(self, query):
        relevant_conversations = self.retrieve_relevant_conversations(query)
        context = "\n".join([conv['text'] for conv in relevant_conversations])
        augmented_query = f"Context:\n{context}\n\nQuery:\n{query}"
        return augmented_query
    
    def clean_conversation(self):
        self.conversationsDB.delete()
        
    def get_n_items(self):
        results = self.conversationsDB.get()
        return results