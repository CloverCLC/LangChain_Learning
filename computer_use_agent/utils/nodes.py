from functools import lru_cache
# from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from computer_use_agent.utils.tools import tools
from langgraph.prebuilt import ToolNode
from langchain_community.llms import Tongyi
import os

api_key = os.getenv("DASHSCOPE_API_KEY")

def call_model(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    model_name = config.get('configurable', {}).get("model_name", "anthropic")
    model = _get_model(model_name)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}
