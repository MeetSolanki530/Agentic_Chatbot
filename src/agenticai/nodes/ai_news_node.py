from src.agenticai.state.state import State
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate



class AINewsNode:

    def __init__(self,llm):
        
        """
        Initialize the AINewsNode with API Keys for Tavily and LLM.
        """
        
        self.tavily = TavilyClient()
        self.llm = llm
        
        # this is used to capture various steps in this filde so that later can be use for steps shown
        self.state = {}


    def fetch_news(self,state: dict) -> dict:
        
        """
        fetch ai news based on the specified frequency.

        Args:
            state (dict): The State dictionary containing 'frequency'.

        Returns:
            dict: updated state with 'news_data' key containing fetched news.
        """

        frequency = state["messages"][0].content.lower()
        self.state["frequency"] = frequency
        time_range_map = {"daily" : 'd',"weekly" : 'w',"monthly":'m',"year" : 'y'}
        days_map = {'daily': 1,'weekly' : 7, 'monthly' : 30, 'year' : 365}

    
        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) technology news india and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=10,
            days=days_map[frequency],
            include_images=True
            # include_domains = [] add only if needed for specific domain
        )

        state['news_data'] = response.get('results',[])
        self.state['news_data'] = state['news_data']
        return state


    def summarize_news(self,state : dict) -> dict:
        
        """
        Summarize the fetched news using an LLM.

        Args:
            State (dict) : The state dictionary containing 'news data'.
        
        Returns:
            dict: Updated state with 'summary' key containing the summarized news.
            
        """

        news_items = self.state["news_data"]
        prompt_template = ChatPromptTemplate.from_messages([
            ("system" , """
            Summarize AI News articles into markdown format. For each item iclude:
            - Date in **YYYY-MM-DD** format in IST timezone.
            - Concise sentences summary from latest news.
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format.
            ### [Date] - [Summary](URL)
            """),
("user","Articles:\n{articles}")])
        
        articles_str = "\n\n".join([
            f"Content : {item.get('content','')}\\URL:{item.get('url','')}\n Date: {item.get('published_date','')}"
            for item in news_items
        ])

        response  = self.llm.invoke(prompt_template.format(articles = articles_str))

        state["summary"] = response.content

        self.state["summary"] = state["summary"]

        return self.state
    

    def save_result(self,state):
        frequency = self.state['frequency']
        summary = self.state["summary"]
        file_name = f"./AINews/{frequency}_summary.md"
        with open(file_name,"w") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        
        self.state["filename"] = file_name
        return self.state


        

