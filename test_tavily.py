import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv ()
os.environ['TAVILY_API_KEY'] = os.getenv ("TAVILY_API_KEY")

tool = TavilySearchResults(max_results=2)
tools = [tool]
response = tool.invoke("What's a 'node' in LangGraph?")
print(response)