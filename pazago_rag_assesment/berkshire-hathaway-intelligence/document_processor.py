import os
import PyPDF2
import tiktoken
from typing import List, Dict
import re

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        return text.strip()
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """Split text into chunks with metadata"""
        chunks = []
        tokens = self.encoding.encode(text)
        
        for i in range(0, len(tokens), self.chunk_size - self.chunk_overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata.update({
                'chunk_id': len(chunks),
                'start_token': i,
                'end_token': i + len(chunk_tokens)
            })
            
            chunks.append({
                'text': chunk_text,
                'metadata': chunk_metadata
            })
        
        return chunks
    
    def process_documents(self, pdf_directory: str) -> List[Dict]:
        """Process all PDFs in directory"""
        all_chunks = []
        
        for filename in os.listdir(pdf_directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(pdf_directory, filename)
                
                # Extract year from filename
                year_match = re.search(r'(\d{4})', filename)
                year = year_match.group(1) if year_match else 'unknown'
                
                text = self.extract_text_from_pdf(pdf_path)
                clean_text = self.clean_text(text)
                
                metadata = {
                    'source': filename,
                    'year': year,
                    'document_type': 'berkshire_letter'
                }
                
                chunks = self.chunk_text(clean_text, metadata)
                all_chunks.extend(chunks)
        
        return all_chunks