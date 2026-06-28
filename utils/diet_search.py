from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2"

)

db = FAISS.load_local(

    "vectorstore/diet_index",

    embeddings,

    allow_dangerous_deserialization=True

)


def search_diet(query):

    docs = db.similarity_search(

        query,

        k=5

    )

    answer = ""

    for doc in docs:

        answer += doc.page_content

        answer += "\n\n"

    return answer