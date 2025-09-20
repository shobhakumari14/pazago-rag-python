import openai
import os
from typing import List, Dict, Generator
from dotenv import load_dotenv

load_dotenv()

class RAGAgent:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.conversation_memory = []
    
    def create_context(self, retrieved_docs: List[Dict], max_tokens: int = 3000) -> str:
        """Create context from retrieved documents"""
        context_parts = []
        current_tokens = 0
        
        for doc in retrieved_docs:
            doc_text = f"Source: {doc['metadata']['source']} ({doc['metadata']['year']})\n{doc['text']}\n"
            doc_tokens = len(doc_text.split()) * 1.3  # Rough token estimation
            
            if current_tokens + doc_tokens > max_tokens:
                break
            
            context_parts.append(doc_text)
            current_tokens += doc_tokens
        
        return "\n---\n".join(context_parts)
    
    def create_prompt(self, query: str, context: str) -> str:
        """Create prompt for the LLM"""
        return f"""You are an expert analyst of Warren Buffett's investment philosophy and Berkshire Hathaway's business strategy. 
Use the provided context from Berkshire Hathaway shareholder letters to answer questions accurately and comprehensively.

Context from Berkshire Hathaway Letters:
{context}

Question: {query}

Instructions:
- Answer based primarily on the provided context
- Include specific quotes when relevant
- Mention the year/source when citing information
- If the context doesn't contain enough information, acknowledge this
- Maintain Warren Buffett's tone and perspective
- Provide actionable insights when possible

Answer:"""
    
    def generate_response(self, query: str, retrieved_docs: List[Dict]) -> str:
        """Generate response using OpenAI API (v0.28)"""
        context = self.create_context(retrieved_docs)
        prompt = self.create_prompt(query, context)
        
        try:
            response = openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                stop=None
            )
            
            return response.choices[0].text.strip()
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def stream_response(self, query: str, retrieved_docs: List[Dict]) -> Generator[str, None, None]:
        """Generate streaming response"""
        context = self.create_context(retrieved_docs)
        prompt = self.create_prompt(query, context)
        
        try:
            response = openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].text:
                    yield chunk.choices[0].text
        
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def add_to_memory(self, query: str, response: str):
        """Add conversation to memory"""
        self.conversation_memory.append({
            'query': query,
            'response': response
        })
        
        # Keep only last 5 conversations
        if len(self.conversation_memory) > 5:
            self.conversation_memory = self.conversation_memory[-5:]
    
    def get_conversation_context(self) -> str:
        """Get recent conversation context"""
        if not self.conversation_memory:
            return ""
        
        context = "Recent conversation:\n"
        for conv in self.conversation_memory[-3:]:  # Last 3 conversations
            context += f"Q: {conv['query']}\nA: {conv['response'][:200]}...\n\n"
        
        return context