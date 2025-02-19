import os
from dotenv import load_dotenv
from state import State
from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import ChatLiteLLM
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition

class ChatbotMemory:
    
    def __init__(self, id):
        load_dotenv ()
        os.environ['DEEPSEEK_API_KEY'] = os.getenv ("DEEPSEEK_API_KEY")
        os.environ['TAVILY_API_KEY'] = os.getenv ("TAVILY_API_KEY")
        self.llm = ChatLiteLLM(model="deepseek/deepseek-chat")
        self.tool = TavilySearchResults(max_results=2)
        self.graph_builder = StateGraph(State)
        self.tool = TavilySearchResults(max_results=2)
        self.tools = [ self.tool]
        self.config = {"configurable": {"thread_id": id}}
        self.memory = MemorySaver()

    def send(self, state: State):
        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    def create_graph(self):
        self.graph_builder.add_node("chatbot", self.send)
        tool_node = ToolNode(tools=[self.tool])
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,
        )
        # Any time a tool is called, we return to the chatbot to decide the next step
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge(START, "chatbot")
        self.graph = self.graph_builder.compile(checkpointer=self.memory)
    
    def stream(self, user_input):
        events = self.graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            self.config,
            stream_mode="values",
        )
        return events
    
    def getGraph(self):
        return self.graph