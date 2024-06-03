from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

