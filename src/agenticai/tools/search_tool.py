from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import Tool
from langgraph.prebuilt import ToolNode
from ddgs import DDGS
import json

def duckduckgo_search_function(query: str) -> str:
    """
    Custom DuckDuckGo search function that returns clean, formatted results
    """
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=5))
        
        if not results:
            return "No search results found for the query."
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No Title')
            snippet = result.get('body', 'No description available')
            link = result.get('href', '')
            
            formatted_results.append({
                'title': title,
                'snippet': snippet,
                'link': link
            })
        
        # Return as JSON string for consistent parsing
        return json.dumps(formatted_results, indent=2)
        
    except Exception as e:
        return f"Search error: {str(e)}"

def get_tools(selected_engine, tavily_key=None):
    """
    Get search tools based on the selected engine
    """
    tools = []
    
    if selected_engine == "TavilySearch" and tavily_key:
        try:
            tavily_tool = TavilySearchResults(
                api_key=tavily_key,
                max_results=5
            )
            tools.append(tavily_tool)
        except Exception as e:
            print(f"Error creating Tavily tool: {e}")
        
    else:  # Default to DuckDuckGo
        # Create a custom tool with a clean interface
        duckduckgo_tool = Tool(
            name="web_search",
            description="Search the web for current information. Use this when you need up-to-date information, news, or facts that you don't already know. Input should be a clear search query.",
            func=duckduckgo_search_function
        )
        tools.append(duckduckgo_tool)
    
    return tools

def create_tool_node(tools):
    """
    Create a tool node from the provided tools
    """
    if not tools:
        raise ValueError("No tools provided to create tool node")
    return ToolNode(tools)







##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------



# Alternative implementation if we want to manually handle DuckDuckGo search
def get_tools_alternative(selected_engine, tavily_key=None):
    """
    Alternative implementation with custom DuckDuckGo tool that doesn't require parse_json
    """
    from langchain_core.tools import Tool
    from duckduckgo_search import DDGS
    
    def duckduckgo_search(query: str) -> str:
        """Custom DuckDuckGo search function that returns formatted results"""
        try:
            ddgs = DDGS()
            results = list(ddgs.text(query, max_results=5))
            
            if not results:
                return "No search results found."
            
            formatted_results = "Search Results:\n\n"
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. **{result.get('title', 'No Title')}**\n"
                formatted_results += f"   {result.get('body', 'No description')}\n"
                formatted_results += f"   Source: {result.get('href', 'No URL')}\n\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Search error: {str(e)}"
    
    tools = []
    
    if selected_engine == "TavilySearch" and tavily_key:
        tavily_tool = TavilySearchResults(
            api_key=tavily_key,
            max_results=5
        )
        tools.append(tavily_tool)
        
    else:
        # Custom DuckDuckGo tool that doesn't need parse_json
        ddg_tool = Tool(
            name="duckduckgo_search",
            description="Search the web using DuckDuckGo. Input should be a search query string.",
            func=duckduckgo_search
        )
        tools.append(ddg_tool)
    
    return tools