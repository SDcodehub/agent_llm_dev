from openai_chat_bot import OpenAIChatBot
from message import Message

if __name__ == "__main__":
    # Prompt the user to enter their OpenAI API key
    api_key = input("Enter your OpenAI API key: ")

    # Create an OpenAIChatBot instance
    chat_bot = OpenAIChatBot(model="gpt-3.5-turbo", api_key=api_key)

    # Trial 1
    message_1 = Message()
    message_1.system("You are a helpful assistant.")
    message_1.user("Who won the world series in 2020?")
    message_1.assistant("The Los Angeles Dodgers won the World Series in 2020.")
    message_1.user("Where was it played?")

    messages_1 = message_1.messages
    response_1 = chat_bot.send_messages_and_get_response(messages_1)

    print("Trial 1 - Assistant's Response:", response_1)

    # Trial 2
    message_2 = Message()
    message_2.system("You are an informative assistant.")
    message_2.user("Tell me about the Eiffel Tower.")
    message_2.assistant("The Eiffel Tower is a famous landmark in Paris, France.")
    message_2.user("How tall is it?")

    messages_2 = message_2.messages
    response_2 = chat_bot.send_messages_and_get_response(messages_2)

    print("Trial 2 - Assistant's Response:", response_2)
