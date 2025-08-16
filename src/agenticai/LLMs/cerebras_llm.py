from langchain_cerebras import ChatCerebras
import os
import streamlit as st


class CerebrasLLM:
    def __init__(self,user_controls_input):
        self.user_controls_input=user_controls_input
    
    def get_llm_models(self):
        try:
            cerebras_api_key=self.user_controls_input["CEREBRAS_API_KEY"]
            
            selected_cerebras_model = self.user_controls_input["selected_cerebras_model"]
            
            if cerebras_api_key == '' and os.environ["CEREBRAS_API_KEY"] == '':
                st.error("Please Enter the Cerebras API Key")
            
            llm = ChatCerebras(api_key=cerebras_api_key,model=selected_cerebras_model)

        except Exception as e:
            raise ValueError(F"Error Occured With Exception : {e}")
        
        return llm
