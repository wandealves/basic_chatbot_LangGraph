import os
from dotenv import load_dotenv
from basic_tool_node import BasicToolNode
from state import State
from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import ChatLiteLLM
from langchain_community.tools.tavily_search import TavilySearchResults

class ChatbotTavily:
    
    def __init__(self):
        load_dotenv ()
        os.environ['DEEPSEEK_API_KEY'] = os.getenv ("DEEPSEEK_API_KEY")
        os.environ['TAVILY_API_KEY'] = os.getenv ("TAVILY_API_KEY")
        self.llm = ChatLiteLLM(model="deepseek/deepseek-chat")
        self.tool = TavilySearchResults(max_results=2)
        self.tools = [self.tool]
        self.tool_node = BasicToolNode(tools=[self.tool])
        self.graph_builder = StateGraph(State)

    def send(self, state: State):
        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    def create_graph(self):
        #self.graph_builder.add_node("chatbot", self.send)
        #self.graph_builder.add_edge(START, "chatbot")
        #self.graph_builder.add_edge("chatbot", END)
        #self.graph = self.graph_builder.compile()

        self.graph_builder.add_node("chatbot", self.send)
        self.graph_builder.add_node("tools", self.tool_node)
        # The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
        # it is fine directly responding. This conditional routing defines the main agent loop.
        self.graph_builder.add_conditional_edges(
        "chatbot",
        self.route_tools,
        # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
        # It defaults to the identity function, but if you
        # want to use a node named something else apart from "tools",
        # You can update the value of the dictionary to something else
        # e.g., "tools": "my_tools"
        {"tools": "tools", END: END},
        )
        # Any time a tool is called, we return to the chatbot to decide the next step
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge(START, "chatbot")
        self.graph = self.graph_builder.compile()

    def route_tools(self,state: State):
        """
        Use in the conditional_edge to route to the ToolNode if the last message
        has tool calls. Otherwise, route to the end.
        """
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return END
    
    def getGraph(self):
        return self.graph