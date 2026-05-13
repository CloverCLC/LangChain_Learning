#reduce [rɪˈdus] v.简化
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.types import Send
from langgraph.graph import StateGraph,START,END
from pydantic import BaseModel,Field
import os

subject_prompt = """请以 JSON 格式生成2到5个关于{topic}的子主题。
必须返回以下格式的JSON：
{{
    "subjects": ["子主题1", "子主题2", "子主题3"]
}}
键名必须是"subjects"。"""

joke_prompt = """以 JSON 格式生成一个关于{subject}的笑话。
必须返回以下格式的JSON：
{{
    "joke": "笑话内容"
}}
键名必须是"joke"。"""

best_joke_prompt = """以下是一些关于{topic}的笑话，请以 JSON 格式选出一个最好的，返回最佳笑话的ID。
必须返回以下格式的JSON：
{{
    "id": 最佳笑话的索引（从0开始）
}}
键名必须是"id"。

{jokes}"""



class Subjects(BaseModel):
    subjects:list[str]

class Joke(BaseModel):
    joke:str

class BestJoke(BaseModel):
    id:int = Field(description="最佳笑话的索引,从0开始",ge=0)

model = ChatOpenAI(
    model="qwen3.6-plus",
    temperature=0,
    api_key=os.environ.get("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class OverallState(TypedDict):
    topic:str
    subjects:list
    # operator.add为了将所有节点生成的joke合并到一个列表里
    jokes:Annotated[list,operator.add]
    best_selected_joke:str

class JokeState(TypedDict):
    subject:str

def generate_topic(state:OverallState):
    prompt = subject_prompt.format(topic=state["topic"])
    res = model.with_structured_output(Subjects).invoke(prompt)
    return {"subjects":res.subjects}

def generate_joke(state:JokeState):
    prompt = joke_prompt.format(subject=state["subject"])
    res = model.with_structured_output(Joke).invoke(prompt)
    return {"jokes":[res.joke]}

def continue_to_joke(state:OverallState):
    return [Send("generate_joke",{"subject":s}) for s in state["subjects"]]

def best_joke(state:OverallState):
    jokes = "\n\n".join(state["jokes"])
    prompt = best_joke_prompt.format(topic=state["topic"],jokes=jokes)
    res = model.with_structured_output(BestJoke).invoke(prompt)
    return {"best_selected_joke":state["jokes"][res.id]}

graph = StateGraph(OverallState)
graph.add_node("generate_topic",generate_topic)
graph.add_node("generate_joke",generate_joke)
graph.add_node("best_joke",best_joke)
graph.add_edge(START,"generate_topic")
graph.add_conditional_edges("generate_topic",continue_to_joke,["generate_joke"])
graph.add_edge("generate_joke","best_joke")
graph.add_edge("best_joke",END)

app = graph.compile()

# res = app.invoke({"topic":"动物"})
for s in app.stream({"topic":"动物"}):
    print(s)
# print(res)
