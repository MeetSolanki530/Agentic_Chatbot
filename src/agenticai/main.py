import streamlit as st
from src.agenticai.ui.streamlitui.load_ui import LoadStreamlitUI
from src.agenticai.LLMs.groq_llm import GroqLLM
from src.agenticai.LLMs.google_llm import GoogleLLM
from src.agenticai.LLMs.openai_llm import OpenAILLM
from src.agenticai.LLMs.cerebras_llm import CerebrasLLM
from src.agenticai.graph.graph_builder import GraphBuilder
from src.agenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the Langgraph AgentiAI Application with streamlit UI.
    This function initiatilizes the UI, handles user input, configures the LLM Model.
    sets up the graph based on the selected use case, adn displays the output while 
    implementing exception handling for robustness.
    
    """

    ## Load UI

    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error : Failed to load user input from the UI")
        return
    
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your Message: ")

    if user_message:
        try:
            #Configure LLM

            # ------------------- LLM Selection -------------------
            selected_llm = user_input.get("selected_llm")
            
            if selected_llm == "Groq":
                obj_llm_config = GroqLLM(user_controls_input=user_input)
            elif selected_llm == "Google":
                obj_llm_config = GoogleLLM(user_controls_input=user_input)
            elif selected_llm == "OpenAI":
                obj_llm_config = OpenAILLM(user_controls_input=user_input)
            elif selected_llm == "Cerebras":
                obj_llm_config = CerebrasLLM(user_controls_input=user_input)
            else:
                st.error(f"Unsupported LLM selected: {selected_llm}")
                return
            # -------------------------------------------------------

            model = obj_llm_config.get_llm_models()

            if not model:
                st.error("Error: LLM Model Could not be initialized.")
            
            ### initialize and set up the graph based on use case
            usecase = user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No Use Case Selected.")
                return
            
            ### Graph Builder
            graph_builder = GraphBuilder(model)

            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase=usecase,graph=graph,user_message=user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error Graph Set up failed - {e}")
                return
            
        except Exception as e:
            st.error(f"Error Graph Set up failed - {e}")
            return



