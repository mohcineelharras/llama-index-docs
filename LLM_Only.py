import streamlit as st
import pandas as pd
import numpy as np
#import torch
from langchain.llms import OpenAI
import os
    

with st.sidebar:
    api_server_info = st.text_input("Local LLM API server", "http://172.19.208.1:1300/v1",key="openai_api_base")
    st.title("🤖 Llama Index 📚")
    st.write("🚀 This app allows you to chat with LLM using LM STUDIO")
    st.subheader("💻 System Requirements: ")
    st.markdown("- CPU: the faster the better ")
    st.markdown("- RAM: 8 GB or higher")
    st.markdown("- GPU: optional but very useful for Cuda acceleration")
    st.subheader("🔑 Developer Information:")
    st.write("This app is developed and maintained by @mohcineelharras")    
    
    


st.title("💬 LLM only")
prompt = st.text_area("Prompt")
if prompt:
    llm = OpenAI(
    openai_api_key = "anyValueYouLike",
    temperature = 0.2,
    openai_api_base = api_server_info,
    max_tokens = 100,
    #...any other options, read the langchain docs for more information if required
    )

    response = llm(prompt=prompt)
    st.write("LLM's Response:\n", response)
