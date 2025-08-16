from langchain_google_genai import ChatGoogleGenerativeAI
import os
import streamlit as st


class GoogleLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input=user_controls_input
    
    def get_llm_models(self):
        try:
            google_api_key=self.user_controls_input["GOOGLE_API_KEY"]
            
            selected_google_model = self.user_controls_input["selected_google_model"]
            
            if google_api_key == '' and os.environ["GOOGLE_API_KEY"] == '':
                st.error("Please Enter the Google API Key")
            
            llm = ChatGoogleGenerativeAI(api_key=google_api_key,model=selected_google_model)

        except Exception as e:
            raise ValueError(F"Error Occured With Exception : {e}")
        
        return llm
