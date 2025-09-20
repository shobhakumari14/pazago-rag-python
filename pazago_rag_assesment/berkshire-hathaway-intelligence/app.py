# import streamlit as st
# import os
# from document_processor import DocumentProcessor
# from vector_store import VectorStore
# from rag_agent import RAGAgent
# import time

# # Page config
# st.set_page_config(
#     page_title="Berkshire Hathaway Intelligence",
#     page_icon="📈",
#     layout="wide"
# )

# # Initialize session state
# if 'vector_store' not in st.session_state:
#     st.session_state.vector_store = None
# if 'rag_agent' not in st.session_state:
#     st.session_state.rag_agent = RAGAgent()
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
# if 'documents_processed' not in st.session_state:
#     st.session_state.documents_processed = False

# def process_documents():
#     """Process PDF documents and build vector store"""
#     pdf_directory = "pdfs"
    
#     if not os.path.exists(pdf_directory):
#         st.error(f"Please create a '{pdf_directory}' folder and add Berkshire Hathaway PDF letters")
#         return False
    
#     pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
#     if not pdf_files:
#         st.error(f"No PDF files found in '{pdf_directory}' folder")
#         return False
    
#     with st.spinner("Processing documents..."):
#         # Process documents
#         processor = DocumentProcessor()
#         chunks = processor.process_documents(pdf_directory)
        
#         # Build vector store
#         vector_store = VectorStore()
#         vector_store.build_index(chunks)
        
#         # Save index
#         vector_store.save_index("berkshire_index")
        
#         st.session_state.vector_store = vector_store
#         st.session_state.documents_processed = True
        
#         st.success(f"Processed {len(chunks)} chunks from {len(pdf_files)} documents")
#         return True

# def load_existing_index():
#     """Load existing vector store index"""
#     vector_store = VectorStore()
#     if vector_store.load_index("berkshire_index"):
#         st.session_state.vector_store = vector_store
#         st.session_state.documents_processed = True
#         return True
#     return False

# def display_sources(retrieved_docs):
#     """Display source documents"""
#     with st.expander("📚 Sources", expanded=False):
#         for i, doc in enumerate(retrieved_docs[:3]):
#             st.write(f"**Source {i+1}:** {doc['metadata']['source']} ({doc['metadata']['year']})")
#             st.write(f"**Relevance Score:** {doc['score']:.3f}")
#             st.write(f"**Excerpt:** {doc['text'][:300]}...")
#             st.divider()

# # Main UI
# st.title("📈 Berkshire Hathaway Intelligence")
# st.markdown("*Ask questions about Warren Buffett's investment philosophy using Berkshire Hathaway shareholder letters*")

# # Sidebar
# with st.sidebar:
#     st.header("🔧 Setup")
    
#     # Document processing
#     if st.button("Process Documents", type="primary"):
#         if process_documents():
#             st.rerun()
    
#     if st.button("Load Existing Index"):
#         if load_existing_index():
#             st.success("Index loaded successfully!")
#             st.rerun()
    
#     # Status
#     if st.session_state.documents_processed:
#         st.success("✅ Documents ready")
#         if st.session_state.vector_store:
#             st.info(f"📊 {len(st.session_state.vector_store.documents)} chunks indexed")
#     else:
#         st.warning("⚠️ Documents not processed")
    
#     st.divider()
    
#     # Sample questions
#     st.header("💡 Sample Questions")
#     sample_questions = [
#         "What does Warren Buffett think about cryptocurrency?",
#         "How has Berkshire's investment strategy evolved?",
#         "What companies did Berkshire acquire recently?",
#         "What is Buffett's view on market volatility?",
#         "How does Buffett evaluate management quality?"
#     ]
    
#     for question in sample_questions:
#         if st.button(question, key=f"sample_{hash(question)}"):
#             st.session_state.current_question = question

# # Main chat interface
# if st.session_state.documents_processed and st.session_state.vector_store:
    
#     # Chat input
#     query = st.chat_input("Ask about Warren Buffett's investment philosophy...")
    
#     # Handle sample question selection
#     if hasattr(st.session_state, 'current_question'):
#         query = st.session_state.current_question
#         delattr(st.session_state, 'current_question')
    
#     # Display chat history
#     for chat in st.session_state.chat_history:
#         with st.chat_message("user"):
#             st.write(chat["question"])
        
#         with st.chat_message("assistant"):
#             st.write(chat["answer"])
#             if "sources" in chat:
#                 display_sources(chat["sources"])
    
#     # Process new query
#     if query:
#         # Add user message
#         with st.chat_message("user"):
#             st.write(query)
        
#         # Generate response
#         with st.chat_message("assistant"):
#             # Retrieve relevant documents
#             with st.spinner("Searching knowledge base..."):
#                 retrieved_docs = st.session_state.vector_store.search(query, k=5)
            
#             if not retrieved_docs:
#                 st.error("No relevant documents found. Please check your query.")
#             else:
#                 # Generate streaming response
#                 response_placeholder = st.empty()
#                 full_response = ""
                
#                 for chunk in st.session_state.rag_agent.stream_response(query, retrieved_docs):
#                     full_response += chunk
#                     response_placeholder.markdown(full_response + "▌")
                
#                 response_placeholder.markdown(full_response)
                
#                 # Display sources
#                 display_sources(retrieved_docs)
                
#                 # Add to chat history
#                 st.session_state.chat_history.append({
#                     "question": query,
#                     "answer": full_response,
#                     "sources": retrieved_docs
#                 })
                
#                 # Add to agent memory
#                 st.session_state.rag_agent.add_to_memory(query, full_response)

# else:
#     # Setup instructions
#     st.info("👆 Please process documents first using the sidebar")
    
#     with st.expander("📋 Setup Instructions", expanded=True):
#         st.markdown("""
#         1. **Create a 'pdfs' folder** in the same directory as this app
#         2. **Download Berkshire Hathaway letters** (2019-2024) from the provided Google Drive link
#         3. **Place PDF files** in the 'pdfs' folder
#         4. **Click 'Process Documents'** in the sidebar
#         5. **Start asking questions** about Warren Buffett's investment philosophy!
        
#         **Sample PDF structure:**
#         ```
#         pdfs/
#         ├── berkshire_2019.pdf
#         ├── berkshire_2020.pdf
#         ├── berkshire_2021.pdf
#         ├── berkshire_2022.pdf
#         ├── berkshire_2023.pdf
#         └── berkshire_2024.pdf
#         ```
#         """)

# # Footer
# st.divider()
# st.markdown("*Built with Streamlit • Powered by OpenAI GPT-4o-mini • Vector Search with FAISS*")





import streamlit as st
import os
from document_processor import DocumentProcessor
from vector_store import VectorStore
from rag_agent import RAGAgent
import time
import plotly.express as px
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Berkshire Hathaway Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .creator-badge {
        position: fixed;
        bottom: 80px;
        right: 20px;
        background: rgba(102, 126, 234, 0.8);
        backdrop-filter: blur(8px);
        color: white;
        padding: 6px 10px;
        border-radius: 15px;
        font-size: 0.7rem;
        z-index: 999;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .creator-badge:hover {
        background: rgba(102, 126, 234, 1);
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .stats-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        color: var(--text-color);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Dark theme compatibility */
    @media (prefers-color-scheme: dark) {
        .stats-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #ffffff;
        }
    }
    
    /* Streamlit dark theme */
    .stApp[data-theme="dark"] .stats-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #ffffff;
    }
    
    /* Force visibility for stats cards */
    .stats-card h3 {
        color: #667eea !important;
        font-size: 2rem !important;
        margin: 0 !important;
        font-weight: bold !important;
    }
    
    .stats-card p {
        color: inherit !important;
        margin: 0 !important;
        opacity: 0.8;
    }
    .question-button {
        margin: 0.2rem 0;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'rag_agent' not in st.session_state:
    st.session_state.rag_agent = RAGAgent()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'documents_processed' not in st.session_state:
    st.session_state.documents_processed = False
if 'processing_stats' not in st.session_state:
    st.session_state.processing_stats = {}

def process_documents():
    """Process PDF documents and build vector store"""
    pdf_directory = "pdfs"
    
    if not os.path.exists(pdf_directory):
        st.error(f"Please create a '{pdf_directory}' folder and add Berkshire Hathaway PDF letters")
        return False
    
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    if not pdf_files:
        st.error(f"No PDF files found in '{pdf_directory}' folder")
        return False
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("Processing documents..."):
        start_time = time.time()
        
        # Process documents
        processor = DocumentProcessor()
        status_text.text("Extracting text from PDFs...")
        progress_bar.progress(25)
        chunks = processor.process_documents(pdf_directory)
        
        # Build vector store
        status_text.text("Building vector embeddings...")
        progress_bar.progress(75)
        vector_store = VectorStore()
        vector_store.build_index(chunks)
        
        # Save index
        status_text.text("Saving index...")
        progress_bar.progress(90)
        vector_store.save_index("berkshire_index")
        
        processing_time = time.time() - start_time
        
        st.session_state.vector_store = vector_store
        st.session_state.documents_processed = True
        st.session_state.processing_stats = {
            'chunks': len(chunks),
            'documents': len(pdf_files),
            'processing_time': processing_time,
            'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        progress_bar.progress(100)
        status_text.text("✅ Complete!")
        
        st.success(f"Processed {len(chunks)} chunks from {len(pdf_files)} documents in {processing_time:.1f} seconds")
        time.sleep(1)  # Brief pause to show completion
        return True

def load_existing_index():
    """Load existing vector store index"""
    vector_store = VectorStore()
    if vector_store.load_index("berkshire_index"):
        st.session_state.vector_store = vector_store
        st.session_state.documents_processed = True
        return True
    return False

def display_sources(retrieved_docs):
    """Display source documents"""
    with st.expander("📚 Sources", expanded=False):
        for i, doc in enumerate(retrieved_docs[:3]):
            st.write(f"**Source {i+1}:** {doc['metadata']['source']} ({doc['metadata']['year']})")
            st.write(f"**Relevance Score:** {doc['score']:.3f}")
            st.write(f"**Excerpt:** {doc['text'][:300]}...")
            st.divider()

def display_analytics():
    """Display analytics dashboard"""
    if st.session_state.processing_stats:
        st.subheader("📊 Document Processing Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{st.session_state.processing_stats['documents']}</h3>
                <p>Documents Processed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{st.session_state.processing_stats['chunks']}</h3>
                <p>Text Chunks</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{st.session_state.processing_stats['processing_time']:.1f}s</h3>
                <p>Processing Time</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{len(st.session_state.chat_history)}</h3>
                <p>Questions Asked</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

# Header with creator info
st.markdown("""
<div class="main-header">
    <h1>📈 Berkshire Hathaway Intelligence</h1>
    <p><i>AI-Powered Investment Wisdom from Warren Buffett's Letters</i></p>
    <small>Created by Shobha Kumari | Powered by Advanced RAG Technology</small>
</div>
""", unsafe_allow_html=True)

# Creator badge
st.markdown("""
<div class="creator-badge">
    💻 Shobha Kumari
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔧 Control Panel")
    
    # Document processing section
    st.subheader("📁 Document Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Process Docs", type="primary", use_container_width=True):
            if process_documents():
                st.rerun()
    
    with col2:
        if st.button("📥 Load Index", use_container_width=True):
            if load_existing_index():
                st.success("Index loaded!")
                st.rerun()
    
    # Status section
    st.subheader("📊 System Status")
    if st.session_state.documents_processed:
        st.success("✅ System Ready")
        if st.session_state.vector_store:
            st.info(f"📚 {len(st.session_state.vector_store.documents)} chunks indexed")
            if st.session_state.processing_stats:
                st.info(f"⏱️ Processed: {st.session_state.processing_stats['processed_at']}")
    else:
        st.warning("⚠️ System Not Ready")
        st.info("👆 Process documents to get started")
    
    st.divider()
    
    # Enhanced sample questions with categories
    st.subheader("💡 Question Categories")
    
    question_categories = {
        "🎯 Investment Strategy": [
            "What does Warren Buffett think about cryptocurrency?",
            "How does Buffett evaluate management quality?",
            "What is Buffett's view on market volatility?"
        ],
        "🏢 Business Operations": [
            "What companies did Berkshire acquire recently?",
            "How has Berkshire's investment strategy evolved?",
            "What does Buffett say about dividend policy?"
        ],
        "📈 Market Insights": [
            "What are Buffett's thoughts on inflation?",
            "How does Berkshire handle economic uncertainty?",
            "What does Buffett think about stock buybacks?"
        ]
    }
    
    for category, questions in question_categories.items():
        with st.expander(category):
            for question in questions:
                if st.button(question, key=f"sample_{hash(question)}", use_container_width=True):
                    st.session_state.current_question = question
    
    st.divider()
    
    # Settings
    st.subheader("⚙️ Settings")
    show_analytics = st.checkbox("Show Analytics", True)
    
    # Clear history
    if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Main content area
if show_analytics and st.session_state.documents_processed:
    display_analytics()

# Main chat interface
if st.session_state.documents_processed and st.session_state.vector_store:
    
    # Chat input with enhanced placeholder
    query = st.chat_input("💬 Ask me anything about Warren Buffett's investment philosophy, Berkshire's strategy, or market insights...")
    
    # Handle sample question selection
    if hasattr(st.session_state, 'current_question'):
        query = st.session_state.current_question
        delattr(st.session_state, 'current_question')
    
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["question"])
        
        with st.chat_message("assistant"):
            st.write(chat["answer"])
            if "sources" in chat:
                display_sources(chat["sources"])
    
    # Process new query
    if query:
        # Add user message
        with st.chat_message("user"):
            st.write(query)
        
        # Generate response
        with st.chat_message("assistant"):
            # Retrieve relevant documents
            with st.spinner("Searching knowledge base..."):
                retrieved_docs = st.session_state.vector_store.search(query, k=5)
            
            if not retrieved_docs:
                st.error("No relevant documents found. Please check your query.")
            else:
                # Generate streaming response
                response_placeholder = st.empty()
                full_response = ""
                
                for chunk in st.session_state.rag_agent.stream_response(query, retrieved_docs):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
                # Display sources
                display_sources(retrieved_docs)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "question": query,
                    "answer": full_response,
                    "sources": retrieved_docs
                })
                
                # Add to agent memory
                st.session_state.rag_agent.add_to_memory(query, full_response)

else:
    # Enhanced setup instructions
    st.info("🚀 **Welcome to Berkshire Hathaway Intelligence!** Let's get you started.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("📋 **Quick Setup Guide**", expanded=True):
            st.markdown("""
            ### 🎯 **3 Simple Steps to Get Started:**
            
            1. **📁 Create PDF Folder**
               - Create a folder named `pdfs` in your app directory
               - This is where you'll store the Berkshire letters
            
            2. **📄 Add Documents**
               - Download Berkshire Hathaway shareholder letters (2019-2024)
               - Place them in the `pdfs` folder with clear names
            
            3. **🔄 Process & Chat**
               - Click "Process Docs" in the sidebar
               - Start asking questions about Warren Buffett's wisdom!
            
            ### 📂 **Recommended File Structure:**
            ```
            your-app/
            ├── pdfs/
            │   ├── berkshire_hathaway_2019.pdf
            │   ├── berkshire_hathaway_2020.pdf
            │   ├── berkshire_hathaway_2021.pdf
            │   ├── berkshire_hathaway_2022.pdf
            │   ├── berkshire_hathaway_2023.pdf
            │   └── berkshire_hathaway_2024.pdf
            └── app.py
            ```
            """)
    
    with col2:
        st.markdown("""
        ### 🎯 **What You Can Ask:**
        - Investment strategies
        - Market predictions
        - Business acquisitions
        - Economic insights
        - Management philosophy
        - Risk assessment
        
        ### 🚀 **Features:**
        - ✅ Real-time search
        - ✅ Source citations
        - ✅ Streaming responses
        - ✅ Chat history
        - ✅ Analytics dashboard
        """)

# Enhanced footer
st.divider()
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 10px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);">
        <small style="color: var(--text-color); opacity: 0.9;">Powered by OpenAI GPT-4o-mini • Vector Search with FAISS • Built with ❤️ using Streamlit</small><br>
        <small style="color: var(--text-color); opacity: 0.8;">📊 Advanced RAG Architecture • 🔍 Semantic Search • 💬 Conversational AI</small>
    </div>
    """, unsafe_allow_html=True)