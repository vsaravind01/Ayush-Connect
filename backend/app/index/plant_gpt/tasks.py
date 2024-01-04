import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain.vectorstores import Qdrant
from langchain.document_loaders import TextLoader
import qdrant_client
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

# plant_gpt imports
from services import get_prompt
from services import get_latest_data
from services import insert_data


load_dotenv(dotenv_path= os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))


def get_vector_store(collection_name):
    client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    embeddings = CohereEmbeddings(model = 'embed-multilingual-v2.0')

    vector_store = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )

    return vector_store


def bacfill(file_path, vector_store):
    loader = TextLoader(file_path)
    document=loader.load()
    docs=document[0].page_content
    text_splitter = CharacterTextSplitter(
        # Set a really small chunk size, just to show.
        separator ='\n\n',
        chunk_size = 100,
        chunk_overlap  = 0,
        length_function = len,
        add_start_index = True,
    )
    docs = text_splitter.create_documents([docs])
    texts = [doc.page_content for doc in docs]

    vector_store.add_texts(texts)


def get_response(user_id, query):
    llm=Cohere()
    doc_store = get_vector_store("plant_docs")
    retriever=doc_store.as_retriever()
    
    rag_bot = ConversationalRetrievalChain.from_llm(llm, retriever, combine_docs_chain_kwargs = {"prompt": get_prompt()})

    chat_history = list()
    latest_data = get_latest_data(user_id)

    for i in latest_data:
        chat_history.append((i['query'], i['response']))

    result = rag_bot({"question": query, "chat_history": chat_history})
    insert_data(user_id, query, result['answer'])

    return result['answer']