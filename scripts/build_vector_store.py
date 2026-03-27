from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

PDF_PATH = "/Users/U756064/Downloads/Physics.pdf"
PERSIST_DIR = "vector_data_base"
COLLECTION_NAME = "reference"

def page_to_lesson(page: int) -> str:
    """
    page is usually 0-based from the loader.
    Adjust ranges after you inspect your PDF once.
    """
    if 1 <= page <= 17:
        return "motion"
    elif 18 <= page <= 34:
        return "force"
    elif 35 <= page <= 52:
        return "energy"
    elif 52 <= page <= 64:
        return "thermodynamics"
    return "other"

def build_vector_db():
    loader = PyPDFLoader(PDF_PATH, mode="page")
    docs = loader.load()

    for d in docs:
        page = d.metadata.get("page", -1)
        lesson = page_to_lesson(page)
        d.metadata["lesson"] = lesson

    # good generic default splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
    )

    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
        collection_name=COLLECTION_NAME,
    )

    print(f"Built vector DB with {len(chunks)} chunks at {PERSIST_DIR}")