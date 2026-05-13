import operator
from typing import Annotated,Sequence
from typing_extensions import TypedDict
import os
from langchain_core.messages import BaseMessage,HumanMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI

model_1 = ChatOpenAI(
    model="qwen3.6-plus",
    temperature=0,
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
model_2 = ChatOpenAI(
    model="deepseek-v4-pro",
    temperature=0,
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
models = {
    "qwen":model_1,
    "deepseek":model_2
}

class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage],operator.add]

def call_llm(state:AgentState,config:RunnableConfig):
    # 读取config配置,默认"qwen"
    model_name = config["configurable"].get("model","qwen")
    model = models[model_name]
    res = model.invoke(state["messages"])
    return {"messages":[res]}

builder = StateGraph(AgentState)
builder.add_node("model",call_llm)
builder.add_edge(START,"model")
builder.add_edge("model",END)
graph = builder.compile()

# 添加config
config = {"configurable":{"model":"deepseek"}}

res = graph.invoke({"messages":[HumanMessage(content="你是谁")]},config=config)
print(res)
