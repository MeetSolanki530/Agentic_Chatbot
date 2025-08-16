import json
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from datetime import datetime

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.debug_logs = []
        self.tool_usage_data = []
        
    def log_debug(self, step, message, data=None):
        """Add debug information to the logs in real-time"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = {
            "timestamp": timestamp,
            "step": step,
            "message": message,
            "data": data
        }
        self.debug_logs.append(log_entry)
        return log_entry
    
    def add_tool_usage(self, tool_name, tool_input, tool_output):
        """Track tool usage for the tool panel"""
        self.tool_usage_data.append({
            "tool_name": tool_name,
            "input": tool_input,
            "output": tool_output,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    
    def display_thinking_panel(self, thinking_placeholder):
        """Display real-time thinking panel"""
        with thinking_placeholder.container():
            with st.expander("🧠 Thinking Process", expanded=False):
                st.write("**Real-time model thinking and processing:**")
                
                for i, log in enumerate(self.debug_logs):
                    # Create status indicators
                    if log["step"] == "initialization":
                        status_icon = "🚀"
                        color = "blue"
                    elif log["step"] == "processing":
                        status_icon = "⚙️"
                        color = "orange"
                    elif log["step"] == "tool_call":
                        status_icon = "🔧"
                        color = "green"
                    elif log["step"] == "ai_thinking":
                        status_icon = "🤔"
                        color = "purple"
                    elif log["step"] == "ai_response":
                        status_icon = "🤖"
                        color = "blue"
                    elif log["step"] == "error":
                        status_icon = "❌"
                        color = "red"
                    else:
                        status_icon = "📝"
                        color = "gray"
                    
                    # Display thinking step
                    st.markdown(f"{status_icon} **[{log['timestamp']}]** {log['message']}")
                    
                    # Show detailed data if available
                    if log["data"]:
                        with st.expander(f"Details", expanded=False):
                            if isinstance(log["data"], (dict, list)):
                                st.json(log["data"])
                            else:
                                st.code(str(log["data"]))
                    
                    if i < len(self.debug_logs) - 1:
                        st.write("↓")
    
    def display_tool_panel(self):
        """Display tool usage panel below AI response"""
        if self.tool_usage_data:
            with st.expander("🔍 Tool Usage Details", expanded=False):
                st.write("**Tools used during this interaction:**")
                
                for i, tool_data in enumerate(self.tool_usage_data):
                    st.write(f"**Tool {i+1}: {tool_data['tool_name']}** ⏰ {tool_data['timestamp']}")
                    
                    # Tool input
                    with st.expander(f"Input to {tool_data['tool_name']}", expanded=False):
                        if isinstance(tool_data['input'], (dict, list)):
                            st.json(tool_data['input'])
                        else:
                            st.write(tool_data['input'])
                    
                    # Tool output
                    with st.expander(f"Output from {tool_data['tool_name']}", expanded=False):
                        if isinstance(tool_data['output'], (dict, list)):
                            st.json(tool_data['output'])
                        else:
                            st.write(tool_data['output'])
                    
                    if i < len(self.tool_usage_data) - 1:
                        st.divider()

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        
        # Clear previous logs and tool data
        self.debug_logs = []
        self.tool_usage_data = []
        
        # STEP 1: Display User Question
        with st.chat_message("user"):
            st.markdown(user_message)
        
        # STEP 2: Create placeholder for thinking panel (will be updated in real-time)
        thinking_placeholder = st.empty()
        
        # STEP 3: Create placeholder for AI response
        ai_response_placeholder = st.empty()
        
        # STEP 4: Create placeholder for tool panel
        tool_panel_placeholder = st.empty()
        
        if usecase == "Basic Chatbot":
            self.log_debug("initialization", f"🚀 Starting Basic Chatbot mode")
            self.display_thinking_panel(thinking_placeholder)
            
            self.log_debug("processing", "📤 Sending message to graph stream...")
            self.display_thinking_panel(thinking_placeholder)
            
            try:
                ai_response_content = ""
                
                for event in graph.stream({"messages": ["user", user_message]}):
                    self.log_debug("processing", f"📥 Received response from model")
                    self.display_thinking_panel(thinking_placeholder)
                    
                    for value in event.values():
                        self.log_debug("ai_response", "✅ Processing AI response...")
                        self.display_thinking_panel(thinking_placeholder)
                        
                        ai_response_content = value["messages"].content
                        
                        # Display AI response
                        with ai_response_placeholder.container():
                            with st.chat_message("assistant"):
                                st.markdown(ai_response_content)
                        
                        self.log_debug("ai_response", f"✅ Successfully displayed response ({len(ai_response_content)} characters)")
                        self.display_thinking_panel(thinking_placeholder)
                        
            except Exception as e:
                self.log_debug("error", f"❌ Error occurred: {str(e)}")
                self.display_thinking_panel(thinking_placeholder)
                
                with ai_response_placeholder.container():
                    with st.chat_message("assistant"):
                        st.error("Sorry, I encountered an error while processing your request.")
        
        elif usecase == "Chatbot With Web":
            self.log_debug("initialization", f"🚀 Starting Web Chatbot mode")
            self.display_thinking_panel(thinking_placeholder)
            
            initial_state = {"messages": [HumanMessage(content=self.user_message)]}
            self.log_debug("processing", "📤 Creating initial state and invoking graph...")
            self.display_thinking_panel(thinking_placeholder)
            
            try:
                self.log_debug("processing", "🔄 Graph processing started...")
                self.display_thinking_panel(thinking_placeholder)
                
                res = graph.invoke(initial_state)
                
                self.log_debug("processing", f"📥 Received {len(res['messages'])} messages from graph")
                self.display_thinking_panel(thinking_placeholder)
                
                ai_response_content = ""
                search_results_data = []
                
                for i, message in enumerate(res["messages"]):
                    if isinstance(message, HumanMessage):
                        self.log_debug("processing", "⏭️ Skipping user message (already displayed)")
                        self.display_thinking_panel(thinking_placeholder)
                        continue
                    
                    elif isinstance(message, ToolMessage):
                        self.log_debug("tool_call", f"🔧 Processing web search results...")
                        self.display_thinking_panel(thinking_placeholder)
                        
                        try:
                            search_data = json.loads(message.content)
                            search_results_data = search_data
                            
                            self.log_debug("tool_call", f"✅ Successfully parsed {len(search_data) if isinstance(search_data, list) else 'unknown'} search results")
                            self.display_thinking_panel(thinking_placeholder)
                            
                            # Add to tool usage tracking
                            self.add_tool_usage("Web Search", user_message, search_data)
                            
                        except json.JSONDecodeError:
                            self.log_debug("tool_call", "⚠️ Could not parse search results as JSON")
                            self.display_thinking_panel(thinking_placeholder)
                            
                            self.add_tool_usage("Web Search", user_message, message.content)
                    
                    elif isinstance(message, AIMessage):
                        if message.content and message.content.strip():
                            self.log_debug("ai_thinking", "🤖 Processing AI response...")
                            self.display_thinking_panel(thinking_placeholder)
                            
                            if not (hasattr(message, 'tool_calls') and message.tool_calls and not message.content.strip()):
                                ai_response_content = message.content
                                
                                self.log_debug("ai_response", f"✅ AI response ready ({len(ai_response_content)} characters)")
                                self.display_thinking_panel(thinking_placeholder)
                
                # Display AI Response
                if ai_response_content:
                    with ai_response_placeholder.container():
                        with st.chat_message("assistant"):
                            st.markdown(ai_response_content)
                
                # Display Tool Panel
                with tool_panel_placeholder.container():
                    self.display_tool_panel()
                
                self.log_debug("processing", "🎉 All processing completed successfully!")
                self.display_thinking_panel(thinking_placeholder)
                            
            except Exception as e:
                self.log_debug("error", f"❌ Critical error: {str(e)}")
                self.display_thinking_panel(thinking_placeholder)
                
                with ai_response_placeholder.container():
                    with st.chat_message("assistant"):
                        st.error("Sorry, I encountered an error while processing your request.")
                
                if st.session_state.get("debug_mode", False):
                    st.write(f"**Debug Info**: {type(e).__name__}: {e}")
                    import traceback
                    st.code(traceback.format_exc())





# # Helper function for the main app
# def create_debug_toggle():
#     """Create a debug mode toggle in the sidebar"""
#     with st.sidebar:
#         st.markdown("### 🔧 Debug Settings")
#         debug_mode = st.toggle("Show Detailed Errors", value=st.session_state.get("debug_mode", False))
#         st.session_state["debug_mode"] = debug_mode
    
#     return debug_mode

# # Usage example:
# """
# # In your main Streamlit app:

# st.title("🦈 Agentic Chatbot")
# user_input = st.text_input("Ask me anything:")

# if user_input:
#     display_handler = DisplayResultStreamlit("Chatbot With Web", graph, user_input)
#     display_handler.display_result_on_ui()
# """