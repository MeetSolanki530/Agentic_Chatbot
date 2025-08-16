from src.agenticai.state.state import State
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage,SystemMessage
from datetime import datetime

class ChabotWithToolNode:
    
    """
    Chatbot logic enhanced with tool integration.
    """

    def __init__(self,model):
        self.llm=model
    
    def process(self,state:State)->dict:
        
        """
        Processes the input state and generates a response with tool integration
        """

        user_input = state["messages"][-1] if state["messages"] else ""

        llm_response = self.llm.invoke([{"role" : "user", "content" : user_input}])

        ### Try to simulate tool-speciific logic (use this if you want to simulate user that we are using tools but internally we aren't)
        tools_response = f"Tool Integration for: '{user_input}'"

        return {"messages" : [llm_response,tools_response]}
    
    def create_chatbot(self, tools):
            llm_with_tools = self.llm.bind_tools(tools)

            def chatbot_node(state):
                print(f"DEBUG: Chatbot node called with {len(state['messages'])} messages")
                
                # Get the conversation history
                messages = state["messages"]
                
                # Add system message for better responses if this is the first call
                if len(messages) == 1 and isinstance(messages[0], HumanMessage):
                    current_date = datetime.now()
                    
                    formatted_date = current_date.strftime("%A, %B %d, %Y")
                    formatted_time = current_date.strftime("%I:%M %p")

                    system_message = SystemMessage(content=f"""You are a helpful AI assistant with access to web search tools.

CURRENT DATE AND TIME: Today is {formatted_date} at {formatted_time}

IMPORTANT: Only use the web search tool when:
- The user asks for current news, recent events, or real-time information
- You need up-to-date facts or data that may have changed recently
- The user specifically requests you to search for something
- Questions about "today", "this week", "recent", "latest", "current" events

For general knowledge questions like "What is AI?", "How does machine learning work?", or basic explanations, answer directly using your existing knowledge WITHOUT using tools.

When you do use the search tool:
1. Use a clear, specific search query
2. After receiving results, provide a comprehensive summary
3. Include relevant details and sources when appropriate
4. When searching for current events, include today's date ({formatted_date}) in your context

Answer the user's question directly and naturally. If they ask about time-sensitive information, always consider that today is {formatted_date}.
                """)
                                                   
                    messages = [system_message] + messages
                
                # Call the LLM with the current conversation state
                response = llm_with_tools.invoke(messages)
                
                print(f"DEBUG: LLM response type: {type(response)}")
                print(f"DEBUG: LLM response has content: {hasattr(response, 'content')}")
                print(f"DEBUG: LLM response has tool_calls: {hasattr(response, 'tool_calls')}")
                
                # Return the complete conversation with the new response
                # Note: Don't include the system message in the returned state to keep it clean
                original_messages = state["messages"]
                updated_messages = original_messages + [response]
                
                print(f"DEBUG: Returning {len(updated_messages)} messages")
                return {"messages": updated_messages}

            return chatbot_node