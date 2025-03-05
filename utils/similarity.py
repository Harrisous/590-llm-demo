import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
import os

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
index_name = "financials"
index = pc.Index(index_name)

# calculate cosine similarity
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# retrieve top_k similar vectors manually
def find_top_k_similar_vectors(index, query_vector, top_k=3, namespace=""):
    # fetch vector IDs from the index metadata
    vector_ids = []
    for ids in index.list(namespace=namespace):
        for id in ids:
            vector_ids.append(id)

    # fetch all vectors and their metadata
    fetched_vectors = index.fetch(vector_ids, namespace=namespace).vectors  # Access the vectors attribute

    # compute similarity scores
    similarities = []
    for vector_id, vector_data in fetched_vectors.items():
        similarity = cosine_similarity(query_vector, vector_data['values'])
        similarities.append((vector_id, similarity, vector_data['metadata']))

    # sort by similarity in descending order and return top_k results
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_k_results = similarities[:top_k]

    # extract and return metadata
    metadata_list = [metadata for _, _, metadata in top_k_results]
    return metadata_list


if __name__ == "__main__":
    # Example usage
    query = ("How's apple's performance in 2024 compared to the previous year?")
    response = client.embeddings.create(
    model="text-embedding-ada-002",
    input=query,
    encoding_format="float"
    )
    query_vector = response.data[0].embedding
    top_k = 2  # Number of top results to retrieve

    # Find top_k similar vectors
    metadata_results = find_top_k_similar_vectors(index, query_vector, top_k)
    print(metadata_results)
    # # Display results
    # print("Metadata of Top K Vectors:")
    # for idx, metadata in enumerate(metadata_results):
    #     print(f"{idx+1}. Metadata: {metadata}")



