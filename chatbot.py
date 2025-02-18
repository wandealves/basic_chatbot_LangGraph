import os
from dotenv import load_dotenv
from state import State
from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import ChatLiteLLM

class Chatbot:
    
    def __init__(self):
        load_dotenv ()
        os.environ['DEEPSEEK_API_KEY'] = os.getenv ("DEEPSEEK_API_KEY")
        self.llm = ChatLiteLLM(model="deepseek/deepseek-chat")
        self.graph_builder = StateGraph(State)

    def send(self, state: State):
      return {"messages": [self.llm.invoke(state["messages"])]}
    
    def create_graph(self):
        self.graph_builder.add_node("chatbot", self.send)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        self.graph = self.graph_builder.compile()