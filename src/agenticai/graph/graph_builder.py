from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import tools_condition,ToolNode
from src.agenticai.state.state import State
from src.agenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.agenticai.tools.search_tool import get_tools,create_tool_node
from src.agenticai.nodes.chatbot_with_tool_node import ChabotWithToolNode
from src.agenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self,model,user_controls=None):
        self.llm = model
        self.graph_builder = StateGraph(State)
        self.user_controls = user_controls or {}
        self.graph_builder = StateGraph(State)

    
    
    def basic_chatbot_build_graph(self):
        """Build a basic chatbot graph using Langgraph
        This Method initializes a chatbot mode using the 'BasicChatbotNode' class
        and integrates it into the graph. The chatbot node is set as both the
        entry and exit point of the graph.
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_build_graph(self,selected_engine=None,tavily_key=None):

        """
        Builds an advanced chatbot graph with tool integration.
        This Method creates a chatbot graph that includes both a chatbot node 
        and a tool node. it defines tools, initializes the chatbot with tool
        capabilities, and sets up conditional and direct edges between nodes.
        The Chatbot node is set as the entry point.
        """
        
        selected_engine = self.user_controls.get("selected_search_engine")
        tavily_key = self.user_controls.get("TAVILY_API_KEY")

        ### Define the tool and tool node

        tools = get_tools(selected_engine, tavily_key)  # now conditional
        if not tools:
            raise ValueError(f"No tools available for engine: {selected_engine}")
            
        tool_node = create_tool_node(tools=tools)
        
        # Create chatbot with tool integration
        obj_chatbot_with_node = ChabotWithToolNode(self.llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools=tools)

        ## Add nodes

        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)

        # Defines Edges
        self.graph_builder.add_edge(START,"chatbot")

        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,
            {
                "tools": "tools",
                "__end__": END
            }
        )
        self.graph_builder.add_edge("tools","chatbot")
        # self.graph_builder.add_edge("chatbot",END)


    def ai_news_builder_graph(self):

        ai_news_node = AINewsNode(self.llm)


        ### added nodes

        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_news_node.save_result)
        

        ### added edges

        self.graph_builder.set_entry_point("fetch_news") # same as START, "fetch_news"
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.add_edge("save_result",END)

    
    def setup_graph(self,usecase : str):

        """
        Sets Up the graph for the selected use case
        """

        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        
        elif usecase =="Chatbot With Web":
            self.chatbot_with_tools_build_graph(
                selected_engine=self.user_controls.get("selected_search_engine"),
                tavily_key=self.user_controls.get("TAVILY_API_KEY")
            )

        elif usecase=="AI News":
            self.ai_news_builder_graph()
        
        return self.graph_builder.compile()

