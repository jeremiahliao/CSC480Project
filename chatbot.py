import openai
import dotenv
import os

dotenv.load_dotenv() 
openai.api_key = os.getenv("OPEN_API_KEY")

def chat_with_AI(prompt):
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    conversations = ""

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        conversations += user_input + "\n"
        response = chat_with_AI(conversations)
        print("Chatbot: ", response)
        conversations += response + "\n"

# ADDITIONAL COMMENTS
# - On line #20, the "You: " inside of the 'input()' command could be changed to whoever the bot is talking to in the terminal.