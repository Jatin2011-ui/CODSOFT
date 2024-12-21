def chatbot():
    print("Hello! I am a simple chatbot. How can I assist you today?")
    print("(Type 'exit' to end the conversation)")
    while True:
        try:
            user_input = input("You: ").strip().lower()
        except OSError:
            print("Chatbot: Input is not supported in this environment. Exiting.")
            break
        if user_input == 'exit':
            print("Chatbot: Goodbye! Have a great day!")
            break
        if "hello" in user_input or "hi" in user_input:
            print("Chatbot: Hello! How can I help you today?")
        elif "your name" in user_input:
            print("Chatbot: I am your friendly chatbot! What's your name?")
        elif "time" in user_input:
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"Chatbot: The current time is {current_time}.")
        elif "weather" in user_input:
            print("Chatbot: I'm not connected to live weather services, but it's always a good idea to carry an umbrella just in case!")
        elif "joke" in user_input:
            print("Chatbot: Why don’t scientists trust atoms? Because they make up everything!")
        elif "bye" in user_input:
            print("Chatbot: Goodbye! Talk to you later!")
            break
        else:
            print("Chatbot: I'm sorry, I didn't understand that. Can you please rephrase?")
if __name__ == "__main__":
    chatbot()
