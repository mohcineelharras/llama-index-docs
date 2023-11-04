import streamlit as st
import pandas as pd
import numpy as np
#import torch
from tqdm.notebook import tqdm
from llama_index.embeddings import InstructorEmbedding
from llama_index import ServiceContext, set_global_service_context
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import os

os.environ["OPENAI_API_KEY"] = "NOOPE"
os.environ["OPENAI_API_BASE"] = "http://172.19.208.1:1300/v1v1"


@st.cache_resource
def load_emb_model():
    embed_model_inst = InstructorEmbedding(model_name="hkunlp/instructor-large")
    service_context = ServiceContext.from_defaults(embed_model=embed_model_inst)
    documents = SimpleDirectoryReader("data").load_data()
    print(f"Number of documents: {len(documents)}")
    index = VectorStoreIndex.from_documents(
        documents, service_context=service_context, show_progress=True)
    return index.as_query_engine()

query_engine = load_emb_model()


with st.sidebar:
    api_server_info = st.text_input("Local LLM API server", os.environ["OPENAI_API_BASE"],key="openai_api_base")
    st.title("🤖 Llama Index 📚")
    st.write("🚀 This page allows you to chat with local documents using LLama_index")
    st.write("This app is developed and maintained by **@mohcineelharras**")
    
    
st.title("💬 LLM RAG QA with database")
prompt = st.text_area("Ask your question here")
if prompt:
    response = query_engine.query(prompt)
    st.write("Your prompt: ", prompt)
    st.write("LLM's Response:\n", response.response)
    with st.expander("Document Similarity Search"):
        #st.write(len(response.source_nodes))
        for i, node in enumerate(response.source_nodes):
            dict_source_i = node.node.metadata
            dict_source_i.update({"Text":node.node.text})
            st.write("Source n°"+str(i+1), dict_source_i)
            #st.write("Source n°"+str(i))
            #st.write("Meta Data :", node.node.metadata)
            #st.write("Text :", node.node.text)
            st.write()
