# Berkshire Hathaway Intelligence - Setup Instructions

## Quick Start

1. **Install Dependencies**
   ```bash
   - pip install -r requirements.txt    
   - or install module one by one from requirements.txt
   ```

2. **Create PDF Directory**
   ```bash
   mkdir pdfs
   ```

3. **Download Berkshire Hathaway Letters**
   - Download PDF letters (2019-2024) from the provided Google Drive link
   - Place them in the `pdfs/` folder
   - Recommended naming: `berkshire_2019.pdf`, `berkshire_2020.pdf`, etc.

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Process Documents**
   - Click "Process Documents" in the sidebar
   - Wait for indexing to complete
   - Start asking questions!

## Sample Questions

- "What does Warren Buffett think about cryptocurrency?"
- "How has Berkshire's investment strategy evolved over the past 5 years?"
- "What companies did Berkshire acquire in 2023?"
- "What is Buffett's view on market volatility and timing?"
- "How does Buffett evaluate management quality in potential investments?"

## Architecture

- **Document Processing**: PyPDF2 for text extraction, chunking with tiktoken
- **Vector Storage**: FAISS with sentence-transformers embeddings
- **RAG Agent**: OpenAI GPT-4o-mini with conversation memory
- **Frontend**: Streamlit with real-time streaming responses
- **Source Attribution**: Metadata tracking with document citations

## Features

✅ PDF document processing and chunking
✅ Vector similarity search with FAISS
✅ Streaming responses from OpenAI
✅ Conversation memory and context
✅ Source attribution and citations
✅ Interactive chat interface
✅ Sample questions for quick testing

## Troubleshooting

- Ensure OpenAI API key is set in `.env` file
- Check that PDF files are in the `pdfs/` directory
- Verify all dependencies are installed correctly
- For streaming issues, check OpenAI API version compatibility