from .chatbot import VishvasChatbot


bot = VishvasChatbot()

while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    result = bot.process_message(user_input)

    print("\nAI Response:")
    print(result)