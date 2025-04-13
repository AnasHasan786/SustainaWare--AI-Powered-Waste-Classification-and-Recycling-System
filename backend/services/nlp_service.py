import json
import os
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch
from dotenv import load_dotenv
from ..schemas.nlp_schemas import NLPResponse, NLPErrorResponse  

class NLPModel:
    def __init__(self, context_path='data/context.json', cache_dir='models/weights/nlp'):
        """
        Initialize the NLP model with QA and sentence embedding models.
        """
        load_dotenv()
        try:
            os.makedirs(cache_dir, exist_ok=True)  # Ensure the directory exists

            self.qa_model = pipeline("question-answering", 
                                     model="distilbert-base-uncased-distilled-squad", 
                                     model_kwargs={"cache_dir": cache_dir}) 

            self.embedder = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=cache_dir)  
            self.context = self.load_context(context_path)
            self.topics = list(self.context.keys())
            self.topic_embeddings = self.embedder.encode(self.topics, convert_to_tensor=True)
        except Exception as e:
            print(f"Error initializing models: {e}")

    def load_context(self, context_path):
        """
        Load context from a JSON file.
        """
        try:
            with open(context_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: {context_path} not found.")
            return {}

    def get_cosine_similarity(self, query):
        """
        Find the most similar response using cosine similarity.
        """
        try:
            query_embedding = self.embedder.encode(query, convert_to_tensor=True)
            similarities = util.cos_sim(query_embedding, self.topic_embeddings)
            best_match_idx = torch.argmax(similarities).item()
            best_topic = self.topics[best_match_idx]
            return self.context.get(best_topic, None)
        except Exception as e:
            print(f"Error calculating cosine similarity: {e}")
            return None

    def get_qa_response(self, query):
        """
        Get a response using a question-answering model.
        """
        try:
            response = self.qa_model(question=query, context=" ".join(self.topics))
            return response['answer']
        except Exception as e:
            print(f"Error generating QA response: {e}")
            return "Sorry, I couldn't process your query."

    def get_response(self, user_input):
        try:
            similar_response = self.get_cosine_similarity(user_input)
            if similar_response:
                return similar_response 

            qa_response = self.get_qa_response(user_input)
            return qa_response 
        
        except Exception as e:
            print(f"Error processing response: {e}")
            return "Failed to process the input text." 


