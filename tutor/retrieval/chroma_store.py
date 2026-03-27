from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def get_vectordb(rag_config):
    embeddings = OpenAIEmbeddings(model=rag_config.embedding_model)

    return Chroma(
        persist_directory=rag_config.persist_dir,
        embedding_function=embeddings,
        collection_name=rag_config.collection_name,
    )