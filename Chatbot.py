#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 22:13:33 2024

@author: shreyabaral
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 22:11:32 2024

@author: shreyabaral
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Wed Jul 31 13:36:22 2024

# @author: shreyabaral

# Import necessary libraries


import streamlit as st  # Streamlit for building web app
from langchain.chains import ConversationalRetrievalChain  # LangChain for conversational retrieval
from langchain_community.embeddings import HuggingFaceEmbeddings  # Hugging Face embeddings for vectorization
from langchain_community.vectorstores import FAISS  # FAISS for vector store
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Text splitter for chunking documents
from langchain_community.document_loaders import WebBaseLoader  # Web document loader
from langchain.document_loaders import TextLoader  # Text document loader
from langchain.document_loaders import PyPDFLoader  # PDF document loader
from langchain_groq import ChatGroq  # ChatGroq for LLM model
import os
st.markdown("""
    <style>
    .st-emotion-cache-8ce5z0 {
        background-color: #000;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# Set environment variable for Groq API key
os.environ['GROQ_API_KEY'] = 'Your Api Key'

# Define the LLM model
# Initialize ChatGroq model
llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")

# Set up Streamlit app
st.title("ChatBot with LLama-3.1")  # App title

# Upload PDF document
st.header("Please Upload your PDF document to proceed")  # Header
pdf_docs = st.file_uploader(
    "Upload your PDF", type="pdf", accept_multiple_files=True)  # File uploader

# Process uploaded PDF documents
documents = []
if pdf_docs:
    for pdf_doc in pdf_docs:
        # Save uploaded file to temporary file
        with open(pdf_doc.name, "wb") as f:
            f.write(pdf_doc.getbuffer())

        # Load PDF file using PyPDFLoader
        loader = PyPDFLoader(pdf_doc.name)
        documents = loader.load()

else:
    st.info("No documents uploaded. Please upload a PDF document to proceed.")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # Initialize chat history

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything?"):

    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)  # Display user input

    with st.chat_message("assistant"):
        # Check if documents is not empty
        if documents:

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500, chunk_overlap=50)  # Initialize text splitter
            all_splits = text_splitter.split_documents(
                documents)  # Split documents into chunks

            # Store chunks in vector store with Hugging Face embeddings
            vectorstore = FAISS.from_documents(all_splits, HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-mpnet-base-v2"))

            # Query against own data using ConversationalRetrievalChain
            chain = ConversationalRetrievalChain.from_llm(llm,
                                                          vectorstore.as_retriever(),
                                                          return_source_documents=True)

            # Get result from chain
            result = chain({"question": prompt, "chat_history": [
                           (message["role"], message["content"]) for message in st.session_state.messages]})

            # Display response
            response = st.write(result['answer'])

        else:
            st.error("No documents loaded. Please upload a valid PDF document.")
    st.session_state.messages.append(
        {"role": "assistant", "content": result['answer']})  # Add response to chat history
