Overview
This repository contains a chatbot application built using Streamlit, LangChain, and Hugging Face libraries. The chatbot is designed to answer specific business-related questions based on uploaded documents.
Features
Upload documents (PDF, Text) related to a specific business
Ask questions related to the uploaded documents
Get answers from a large language model (LLM) fine-tuned for business-specific queries
Technical Details
Built using Streamlit for web app development
Utilizes LangChain for conversational retrieval and Hugging Face embeddings for vectorization
FAISS vector store for efficient document retrieval
Supports multiple document loaders (Web, Text, PDF)
ChatGroq LLM model for answering business-specific questions
Usage
Upload a document related to your business
Ask a question related to the uploaded document
Get an answer from the LLM model
UI
The chatbot UI is hosted on https://chatbot-r.streamlit.app/ and can be accessed .
Future Development
Improve document processing and vectorization for better accuracy
Fine-tune LLM model for specific business domains
Add more document loaders and support for additional file formats
