from langchain_community.vectorstores import FAISS  # Updated import
from langchain_community.embeddings import HuggingFaceEmbeddings  # Updated import for embeddings
from langchain_community.llms import Ollama  # Updated import for Ollama
from langchain.chains import RetrievalQA
from git import Repo
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter, Language

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

import streamlit as st

# Create embeddings using Hugging Face
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.load_local("vector_store_index",embeddings, allow_dangerous_deserialization=True )

# Initialize Ollama for the LLM
llm = Ollama(model="deepseek-coder-v2")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Set up a retrieval-based QA chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,  # Your Ollama model
    retriever=vectorstore.as_retriever(),  # Your FAISS retriever
    memory=memory  # Add memory
)

# Streamlit chat interface
st.title("Chat with Codebase")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # Use the qa_chain to generate a response
        response = qa_chain({"question": st.session_state.messages[-1]["content"]})
        
        # Write the response to the stream
        st.write(response["answer"])
        
        # Append the assistant's response to the session state messages
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})    