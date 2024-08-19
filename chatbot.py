#Chatbot using OpenAI API key
#API Key can be loaded in a more secure way
#Chatbot is multilingual
import openai
import os

# Load your API key from an environment variable or secret management service
openai.api_key = "***********************"

def chatbot():
    # Keep repeating the following
    while True:
        # Prompt user for input
        message = input("User: ")

        # Exit program if user inputs "quit"
        if message.lower() == "quit":
            print("Goodbye!")
            break

        # Generate a response using OpenAI's API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can specify the model you want to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        # Print the response from the chatbot
        print("Bot:", response.choices[0].message['content'])

if __name__ == "__main__":
    print("Start chatting with the bot (type 'quit' to stop)!")
    chatbot()
