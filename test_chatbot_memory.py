from chatbot_memory import ChatbotMemory

chatbot = ChatbotMemory("1")
chatbot.create_graph()

def stream_graph_updates(user_input: str):
    for event in chatbot.stream(user_input):
        event["messages"][-1].pretty_print()

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break