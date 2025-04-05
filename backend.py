from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_huggingface import HuggingFacePipeline
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import create_tool_calling_agent
from langchain import hub
from langchain.agents import AgentExecutor
from typing import Literal
import streamlit as st
#from langchain_google_community.calendar.current_datetime import GetCurrentDatetime
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_mistralai.chat_models import ChatMistralAI
from langgraph.prebuilt import create_react_agent
import json
import http.client
import os

load_dotenv()
from langchain.prompts import ChatPromptTemplate
class CricketAPI:
    def __init__(self):
        self.api_key = os.getenv("CRICKET_API_KEY")
        self.host = "cricket-live-line1.p.rapidapi.com"
    
    def _make_request(self, endpoint):
        conn = http.client.HTTPSConnection(self.host)
        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': self.host
        }
        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))

    def fetch_past_matches(self):
        data = self._make_request("/recentMatches")
        match_info = {'match': []}
        date_wise_dict = {}
        
        for match_data in data["data"]:
            date_key = match_data["date_wise"]
            if date_key not in date_wise_dict:
                date_wise_dict[date_key] = []
            date_wise_dict[date_key].append(match_data)

        for date, matches in date_wise_dict.items():
            for match in matches:
                match_info['match'].append({
                    'match_id': match['match_id'],
                    'teams': f"{match['team_a']} vs {match['team_b']}"
                })
        return match_info

    def fetch_live_matches(self):
        data = self._make_request("/liveMatches")
        match_details = {'matches': []}
        for match in data['data']:
            match_details['matches'].append({
                'title': match['series'],
                'id': match['match_id']
            })
        return match_details
    


class ChatAgent(CricketAPI):
    def __init__(self,match_type,user_input, match_id):
        super().__init__()  
        self.memory = MemorySaver()
        self.model = ChatMistralAI(model_name="mistral-large-latest")
        self.search = TavilySearchResults(max_results=2)
        self.match_id= match_id
        self.match_type= match_type
       
    def chat_past_matches(self,*args, **kwargs):
        return self._make_request(f"/match/{self.match_id}/scorecard")
    def chat_match_details(self,*args, **kwargs):
      
        return self._make_request(f"/match/{self.match_id}/scorecard")  
    def tool_selection(self,*args, **kwargs):
        websearch_tool = Tool(name="SportsWebSearch", func=self.search.run, description="Use this tool for general_search.")
        match_info_tool = Tool(name="MatchInfo", func=self.chat_match_details, description="Use this tool to get the live match data It will take match_id as input.")
        past_matches_tool = Tool(name="PastMatches", func=self.chat_past_matches, description="Use this tool to get the past match data. it will take match_id as input.")
        tools=[]
        if self.match_type == "Live":
            tools = [match_info_tool]
        elif self.match_type == "Past":
            tools = [past_matches_tool]
        else:  # Default case (e.g., live matches)
            tools = [websearch_tool]
        return tools
    def get_response(self, user_input, match_type, match_id):
        prompt = f"Match Type: {match_type}, Match ID: {match_id}, Query: {user_input}"
        messages = {"messages": [HumanMessage(content=prompt)]}
        response = ""
        # for step in self.agent_executor.stream(messages, {}, stream_mode="values"):
        #     response = step["messages"][-1].content
        # return response
        tools= self.tool_selection()
        agent_executor = create_react_agent(self.model,tools, checkpointer=self.memory)
        config = {"configurable": {"thread_id": "abc123"}}
        # print("-------------------------------------------------")
        ans=''
        for step in agent_executor.stream(messages, config, stream_mode="values"):
            ans=step["messages"][-1]
            step["messages"][-1].pretty_print()
        return ans.content
