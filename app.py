import streamlit as st
import pandas as pd
import numpy as np
import torch
from tqdm.notebook import tqdm
from llama_index.embeddings import InstructorEmbedding
from llama_index import ServiceContext, set_global_service_context
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import os

@st.cache_resource
def load_emb_model():
    os.environ["OPENAI_API_KEY"] = "NOOPE"
    os.environ["OPENAI_API_BASE"] = "http://172.19.208.1:1300/v1"

    embed_model_inst = InstructorEmbedding(model_name="hkunlp/instructor-large")
    service_context = ServiceContext.from_defaults(embed_model=embed_model_inst)
    documents = SimpleDirectoryReader("data").load_data()
    print(f"Number of documents: {len(documents)}")

    index = VectorStoreIndex.from_documents(
        documents, service_context=service_context, show_progress=True)

    return index.as_query_engine()

query_engine = load_emb_model()


    

def create_sidebar():
    st.title("🤖 Llama Index 📚")
    st.write("🚀 This app allows you to chat with local documents using LLama_index, Streamlit, Pandas, NumPy, and Hugging Face Transformers.")
    st.subheader("💻 System Requirements: ")
    st.markdown("- CPU: the faster the better ")
    st.markdown("- RAM: 8 GB or higher")
    st.markdown("- GPU: optional but very useful for Cuda acceleration")
    st.subheader("🔑 Developer Information:")
    st.write("This app is developed and maintained by @mohcineelharras")    
    
def create_main_content(query_engine):
    st.title("💬 LLM RAG QA")
    prompt = st.text_area("Ask your question here")
    if prompt:
        response = query_engine.query(prompt)
        st.write("Your prompt: ", prompt)
        st.write("LLM's Response:\n", response.response)
    
if __name__ == '__main__':
    with st.sidebar:
        create_sidebar()
    create_main_content(query_engine)
    #st.run()