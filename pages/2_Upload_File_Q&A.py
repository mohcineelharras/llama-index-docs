import streamlit as st
from llama_index.embeddings import InstructorEmbedding
from llama_index import ServiceContext
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import os

os.environ["OPENAI_API_KEY"] = "NOOPE"
os.environ["OPENAI_API_BASE"] = "http://172.19.208.1:1300/v1"

@st.cache_resource
def load_emb_uploaded_document(filename):
    # You may want to add a check to prevent execution during initialization.
    if 'init' in st.session_state:
        embed_model_inst = InstructorEmbedding(model_name="hkunlp/instructor-large")
        service_context = ServiceContext.from_defaults(embed_model=embed_model_inst)
        documents = SimpleDirectoryReader(input_files=[filename]).load_data()
        index = VectorStoreIndex.from_documents(
            documents, service_context=service_context, show_progress=True)
        return index.as_query_engine()
    return None


with st.sidebar:
    api_server_info = st.text_input("Local LLM API server", os.environ["OPENAI_API_BASE"],key="openai_api_base")
    st.title("🤖 Llama Index 📚")
    st.write("🚀 Upload & Query: Instant Answers on the Go!")
    st.write("This app is developed and maintained by **@mohcineelharras**")
    
st.title("📝 One single document Q&A with Llama Index using local open llms")
uploaded_file = st.file_uploader("Upload an File", type=("txt", "csv", "md","pdf"))
question = st.text_input(
    "Ask something about the files",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if 'init' not in st.session_state:
    st.session_state.init = True

# if 'previous_uploaded_file' not in st.session_state:
#     st.session_state.previous_uploaded_file = None

# # Function to check if the uploaded file has changed
# def uploaded_file_changed(uploaded_file):
#     if uploaded_file != st.session_state.previous_uploaded_file:
#         st.session_state.previous_uploaded_file = uploaded_file
#         return True
#     return False

# if uploaded_file:
#     if uploaded_file_changed(uploaded_file):
#         with open("data/"+uploaded_file.name, "wb") as f:
#             text = uploaded_file.read()
#             f.write(text)
#         load_emb_uploaded_document.clear()
#         query_engine = load_emb_uploaded_document("data/"+uploaded_file.name)
#         st.write("File ",uploaded_file.name, "was loaded successfully")

if uploaded_file:
    with open("data/"+uploaded_file.name, "wb") as f:
        text = uploaded_file.read()
        f.write(text)
    load_emb_uploaded_document.clear()
    query_engine = load_emb_uploaded_document("data/"+uploaded_file.name)
    st.write("File ",uploaded_file.name, "was loaded successfully")

if uploaded_file and question and api_server_info:
    response = prompt = f"""Based on the context presented. Respond to the question below to the best of your ability.
    \n\n{question}"""
    response = query_engine.query(prompt)
    st.write("### Answer")
    st.write(response.response)
    with st.expander("Document Similarity Search"):
        #st.write(len(response.source_nodes))
        for i, node in enumerate(response.source_nodes):
            dict_source_i = node.node.metadata
            dict_source_i.update({"Text":node.node.text})
            st.write("Source n°"+str(i+1), dict_source_i)
            #st.write("Source n°"+str(i))
            #st.write("Meta Data :", node.node.metadata)
            #st.write("Text :", node.node.text)
            #st.write()
print(uploaded_file==True, question==True, api_server_info==True)
