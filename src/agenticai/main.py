import streamlit as st
from src.agenticai.ui.streamlitui.load_ui import LoadStreamlitUI


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
    
    user_message = st.chat_input("Enter your Message: ")

    # if user_message:
    #     try:
    #         #Configure LLM
    #         obj_llm_config = (user_controls_input=user_input)
    #         model = obj_llm_config.get_llm_model()

    #         if not model:
    #             st.error("Error: LLM Model Could not be initialized.")
            
    #         ### initialize and set up the graph based on use case
    #         usecase = user_input.get("selected_usecase")

    #         if not usecase:
    #             st.error("Error: No Use Case Selected.")
    #             return


