try:
    import openai
except ModuleNotFoundError:
    print("Error: The 'openai' module is not installed. Please install it using 'pip install openai' before running this script.")
    exit()

openai.api_key = "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"

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except openai.error.OpenAIError as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    print("Chatbot: Hello! Type 'quit', 'exit', or 'bye' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        response = chat_with_gpt(user_input)
        print("Chatbot:", response)
