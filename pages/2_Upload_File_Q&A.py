import streamlit as st
from llama_index.embeddings import InstructorEmbedding
from llama_index import ServiceContext
from llama_index import VectorStoreIndex, SimpleDirectoryReader

@st.cache_resource
def load_emb_uploaded_document(filename):
    embed_model_inst = InstructorEmbedding(model_name="hkunlp/instructor-large")
    service_context = ServiceContext.from_defaults(embed_model=embed_model_inst)
    documents = SimpleDirectoryReader(input_files=[filename]).load_data()
    print(f"Number of documents: {len(documents)}")
    index = VectorStoreIndex.from_documents(
        documents, service_context=service_context, show_progress=True)
    return index.as_query_engine()



with st.sidebar:
    api_server_info = st.text_input("Local LLM API server", "http://172.19.208.1:1300/v1",key="openai_api_base")
    st.title("🤖 Llama Index 📚")
    st.write("🚀 Upload & Query: Instant Answers on the Go!")
    
    
st.title("📝 Documents Q&A with Llama Index using local open llms")
uploaded_file = st.file_uploader("Upload an File", type=("txt", "csv", "md","pdf"))
question = st.text_input(
    "Ask something about the files",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file:
    with open("data/"+uploaded_file.name, "wb") as f:
        text = uploaded_file.read()
        f.write(text)
    load_emb_uploaded_document.clear()
    query_engine = load_emb_uploaded_document("data/"+uploaded_file.name)

if uploaded_file and question and not api_server_info:
    st.info("Please add your Local LLM API server info to continue.")

if uploaded_file and question and api_server_info:
    article = uploaded_file.read().decode()
    response = prompt = f"""Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question}"""
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
            st.write()