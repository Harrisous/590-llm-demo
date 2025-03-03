# reference: https://platform.openai.com/docs/api-reference/embeddings
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

text_list = ["Hello this is a project", "nice to meet you"]

response = client.embeddings.create(
  model="text-embedding-ada-002",
  input=text_list,
  encoding_format="float"
)

# embedding = response.data[0].embedding
embedding_data = response.data
count = 0

for i in range(len(embedding_data)):
  count += 1
  print(embedding_data[i])

print(count)