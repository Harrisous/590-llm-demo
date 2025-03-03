import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
from datetime import datetime

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

index_name = "financials"
# connect to index
index = pc.Index(index_name)
# view index stats
print(index.describe_index_stats())

# user query
current_date = datetime.now().strftime("%A, %B %d, %Y")
query = (
    # "what is the revenue of Apple company in 2024?",
    "How's apple's performance in 2024 compared to the previous year?"
)
response = client.embeddings.create(
  model="text-embedding-ada-002",
  input=query,
  encoding_format="float"
)
embedding = response.data[0].embedding

# make query
res = index.query(vector=embedding, top_k=5, include_metadata=True)

# return answer merged into prompt
prompt = f"""
You are an AI assistant that answers questions based on provided context. The overall answer style should be finiancial. and you will not answer anything not related.
Today's date is {current_date}.
Here is some context:\n
{res['matches']}
Current 
Question: {query}
Answer(in markdown format):
"""
response = client.chat.completions.create(
        model="gpt-4o",  # Replace with "gpt-4" if available and needed
        messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": prompt}
        ],
        temperature=0.9
)
assistant_reply = response.choices[0].message.content
print(assistant_reply)