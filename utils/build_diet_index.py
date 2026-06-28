from pathlib import Path
from pypdf import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import HuggingFaceEmbeddings


# PDF location
PDF_PATH = Path("data/Complete_Diet_Guide.pdf")


def load_pdf():

    reader = PdfReader(PDF_PATH)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


def create_vector_database():

    print("Reading PDF...")

    text = load_pdf()

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )

    chunks = splitter.split_text(text)

    print(f"Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2"

    )

    db = FAISS.from_texts(

        chunks,

        embedding=embeddings

    )

    db.save_local("vectorstore/diet_index")

    print("Diet Index Created Successfully")


if __name__ == "__main__":

    create_vector_database()