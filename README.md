# Assignment 3
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/a87xfYGP)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=18319817)

## Assignment Objective
Build and deploy a LLM application using Retrieval Augmented Generation
(RAG) to improve response performance in a specific domain

## Deliverables
- 10 minute video describing your project 
    - Objective, Data, Pipeline, Model, Performance evaluation, Do NOT show code!
- GitHub repo
## Project Introduction
This project uses RAG to enhance the performance in financial industry.

## Requirements:
- You can use any model you prefer, including via API
- You may NOT use a framework for RAG (e.g. no LangChain etc). You must
write pipelines to:
    - Extract your text data (can use library for parsing only)
    - Chunk it
    - Store it in a database
    - Perform a retrieval using semantic search
    - Insert relevant context into the LLM prompt
- must be deployed on the cloud.

## Running Instruction (for local hosting)
- Step 1. Run clone the GitHub repo and create venv.
- Step 2. Install necessary libraries `pip install -r requirements.txt`
- Step 3. Add a .env file with OpenAI api key `OPENAI_API_KEY=<your API key>`
- Step 4. Search "# for local deployment" and change the secrete loading method; Run `streamlit run app.py` for local hosting.
For preparing data, run `python preparation.py`
## Reference:
Embedding: https://platform.openai.com/docs/api-reference/embeddings
LLM output: https://platform.openai.com/docs/api-reference/chat
Data API: https://site.financialmodelingprep.com/
Pinecone API: https://docs.pinecone.io/guides/get-started/quickstart
