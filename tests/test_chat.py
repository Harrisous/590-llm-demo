from openai import OpenAI
from dotenv import load_dotenv
import os

# set openai key
load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Initialize the chat history
messages = [{
    "role": "system", 
    "content": "You are a helpful assistant."
}]

print("Chat with the assistant! Type 'exit' to end the conversation.")

while True:
    # Get user input
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Exiting chat. Goodbye!")
        break

    # Add user message to the conversation history
    messages.append({"role": "user", 
                     "content": user_input})

    # Generate a response from the assistant
    # try:
    response = client.chat.completions.create(
        model="gpt-4o",  # Replace with "gpt-4" if available and needed
        messages=messages
    )
    assistant_reply = response.choices[0].message.content
    print(f"Assistant: {assistant_reply}")

    # Add assistant response to the conversation history
    messages.append({"role": "assistant", "content": assistant_reply})
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    