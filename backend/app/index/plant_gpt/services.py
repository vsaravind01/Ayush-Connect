import os
from datetime import datetime
import pytz
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate


load_dotenv(dotenv_path= os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))


def get_collection(db_name = "plant_gpt_chat_history", collection_name = "v1"):
    client = MongoClient(os.getenv("MONGO_DB_URL"))
    db = client[db_name]
    collection = db[collection_name]

    return collection


def insert_data(user_id, query, response, collection = get_collection()):
    # Get the current UTC time
    current_time_utc = datetime.utcnow()

    # Define the IST timezone
    ist_timezone = pytz.timezone('Asia/Kolkata')

    # Convert the UTC time to IST
    current_time_ist = current_time_utc.astimezone(ist_timezone)

    # Create a document to insert
    data_to_insert = {
        # "_id": ObjectId(),  # Use ObjectId to generate a unique _id for each document
        "user_id": user_id,
        "chat_history": {
            "query": query,
            "response": response,
            "timestamp": current_time_ist.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        }
    }

    # Insert the document into the collection
    collection.insert_one(data_to_insert)


def get_latest_data(user_id, collection = get_collection()):
    ist_timezone = pytz.timezone('Asia/Kolkata')

    # Find the documents for the given user_id, sort by timestamp in descending order, and limit to 5
    cursor = collection.find(
        {"user_id": user_id}
    ).sort("chat_history.timestamp", pymongo.DESCENDING).limit(5)

    latest_data = []

    for document in cursor:
        # timestamp_ist = datetime.strptime(document["chat_history"]["timestamp"], "%Y-%m-%d %H:%M:%S %Z")
        # timestamp_ist = timestamp_ist.replace(tzinfo=ist_timezone)

        data_entry = {
            "query": document["chat_history"]["query"],
            "response": document["chat_history"]["response"],
            "timestamp": document["chat_history"]["timestamp"]
        }

        latest_data.append(data_entry)

    return latest_data


def get_prompt():
    # prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    # {context}

    # Question: {question}
    # Answer in English:"""


    prompt_template = """You are a chat bot named PLANT GPT and it is your duty to provide answers to the question: {question}
        Do not use technical words, give easy/
        to understand responses.
        {context}
        Answer in English:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["question", "context"]
    )

    prompt_formatted_str: str = prompt_template.format(
    question="Why won't a vehicle start on ignition?",
    language="English")

    return PROMPT
