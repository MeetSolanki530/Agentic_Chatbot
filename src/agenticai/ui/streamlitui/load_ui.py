import streamlit as st
import os

# import Config File
from src.agenticai.ui.ui_config import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls = {}
    
    def load_streamlit_ui(self):
        st.set_page_config(page_title=" 🦈 " + self.config.get_page_title(),layout="wide")
        st.header("🦈 " + self.config.get_page_title())
    

        with st.sidebar:
            #Get Options from config

            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            ### LLM Selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM",llm_options)

            ### Model Selection

            if self.user_controls["selected_llm"] == 'Groq':
                ### Model Options
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model",model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("Groq API Key",type="password")

                # Validate API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please Enter Your Groq API Key To proceed. https://console.groq.com/keys")


            if self.user_controls["selected_llm"] == 'OpenAI':
                ### Model Options
                model_options = self.config.get_openai_model_options()
                self.user_controls["selected_openai_model"] = st.selectbox("Select Model",model_options)
                self.user_controls["OPENAI_API_KEY"] = st.session_state["OPENAI_API_KEY"] =  st.text_input("OpenAI API Key",type="password")

                # Validate API Key
                if not self.user_controls["OPENAI_API_KEY"]:
                    st.warning("⚠️ Please Enter Your OpenAI API Key To proceed. https://platform.openai.com/account/api-keys")

            if self.user_controls["selected_llm"] == 'Google':
                ### Model Options
                model_options = self.config.get_google_model_options()
                self.user_controls["selected_google_model"] = st.selectbox("Select Model",model_options)
                self.user_controls["GOOGLE_API_KEY"] =  st.session_state["GOOGLE_API_KEY"] = st.text_input("Google API Key",type="password")
                
                # Validate API Key
                if not self.user_controls["GOOGLE_API_KEY"]:
                    st.warning("⚠️ Please Enter Your Google API Key To proceed. https://aistudio.google.com/app/apikey")


            if self.user_controls["selected_llm"] == 'Cerebras':
                ### Model Options
                model_options = self.config.get_cerebras_model_options()
                self.user_controls["selected_cerebras_model"] = st.selectbox("Select Model",model_options)
                self.user_controls["CEREBRAS_API_KEY"] = st.session_state["CEREBRAS_API_KEY"] = st.text_input("Cerebras API Key",type="password")

                # Validate API Key
                if not self.user_controls["CEREBRAS_API_KEY"]:
                    st.warning("⚠️ Please Enter Your Cerebras API Key To proceed. https://inference.cerebras.ai/")

            ## Usecase Selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecases",usecase_options)

            if self.user_controls["selected_usecase"] == "Chatbot With Web":
                # self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Enter Tavily API Key: ",type="password")
                self.user_controls["selected_search_engine"] = st.selectbox("Select Web Search Engine", self.config.get_web_search_providers())

                if self.user_controls["selected_search_engine"] == "TavilySearch":
                    os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Enter Tavily API Key: ", type="password")
                    
                    # validate API Key
                    if not self.user_controls["TAVILY_API_KEY"]:
                        st.warning("⚠️ Please enter your TAVILY_API_KEY to proceed https://app.tavily.com/home")
                
                else:
                    # For DuckDuckGo no key needed
                    self.user_controls["TAVILY_API_KEY"] = None
                
        return self.user_controls           
            
