# this file will chunk the data and upload the data from \data to Pinecone vector database
import os
import json
import time
import random
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

# load api to update pinecone data and load api for openai embedding
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

index_name = "financials"
if index_name not in pc.list_indexes().names(): # create index if not existing
    pc.create_index(
        name=index_name,
        dimension=1536, 
        metric="cosine", # metric
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
    )

# connect to index
index = pc.Index(index_name)
response = index.delete(delete_all=True) # clear the index everytime

# view index stats
print(index.describe_index_stats())

# chunk data and upload to Pinecone via index
data_folder = "data"
for filename in os.listdir(data_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(data_folder, filename)
        
        # open and load the JSON file
        with open(file_path, "r", encoding="utf-8") as json_file:
            try:
                financial_data = json.load(json_file)
                print(f"\nProcessing file: {filename}")
                
                for year_data in financial_data:
                    updated_year_data = {key: ("null" if value is None else value) for key, value in year_data.items()} # get rid of null for some values
                    chunk_text = "\n".join([f"{key}: {value}" for key, value in updated_year_data.items()]) # convert json to text for embedding
                    # creating id
                    timestamp = int(time.time() * 1000) # timestamp as id
                    random_number = random.randint(10000, 99999) # addd extra uniqueness
                    unique_id = f"{timestamp}_{random_number}"

                    # creating embedding vector
                    response = client.embeddings.create(
                        model="text-embedding-ada-002",
                        input=chunk_text,
                        encoding_format="float"
                    )
                    embedding = response.data[0].embedding

                    # create meta data for response
                    metadata = updated_year_data # json format

                    # insert into Pinecone database
                    index.upsert(
                        vectors=[
                            {
                                "id": unique_id,
                                "values": embedding,
                                "metadata": metadata
                            }
                        ]
                    )
                       
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")