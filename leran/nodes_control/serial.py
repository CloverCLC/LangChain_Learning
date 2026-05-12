# serial 串行
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END

class State(TypedDict):
    value_1:str
    value_2:str

def step_1(state:State):
    return {
        "value_1":"a"
    }
def step_2(state:State):
    currect_value_1 = state["value_1"]

    return {
        "value_1":f"{currect_value_1} + b"
    }
def step_3(state:State):
    return {
        "value_2":"10"
    }

graph_builder = StateGraph(State)
graph_builder.add_node(step_1)
graph_builder.add_node(step_2)
graph_builder.add_node(step_3)

# 串行编排 START -> step_1 -> step_2 -> step_3 -> END
graph_builder.add_edge(START,"step_1")
graph_builder.add_edge("step_1","step_2")
graph_builder.add_edge("step_2","step_3")
graph_builder.add_edge("step_3",END)

graph = graph_builder.compile()
res = graph.invoke({"value_1":"c"})
print(res)

