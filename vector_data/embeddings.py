from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import TokenTextSplitter

from pypdf import PdfReader

from dotenv import load_dotenv
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

text_splitter = TokenTextSplitter(
    chunk_size=350,
    chunk_overlap=100,
)


def extract_text_pdf(document):
    reader = PdfReader(document)
    pages = reader.pages
    content = ""
    for page in pages:
        content += page.extract_text()
    return content


def splitter_documents(pdf_text):
    documents = text_splitter.split_text(pdf_text)
    return documents


def vectorize_data(chunks):
    vector_db = FAISS.from_texts(chunks, embeddings)
    vector_db.save_local("faiss", "faiss_database")