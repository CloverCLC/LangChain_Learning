import operator
# Literal 是 Python 的「类型提示」工具，专门用来限制变量只能取指定的几个固定值
from typing import Annotated,Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END


# Annotated
class State(TypedDict):
    aggregate:Annotated[list,operator.add]

def a(state:State):
    print(f"添加'A'到{state['aggregate']}")
    return {"aggregate":['A']}
def b(state:State):
    print(f"添加'B'到{state['aggregate']}")
    return {"aggregate":['B']}
def c(state:State):
    print(f"添加'C'到{state['aggregate']}")
    return {"aggregate":['C']}
def d(state:State):
    print(f"添加'D'到{state['aggregate']}")
    return {"aggregate":['D']}


builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)
builder.add_node(c)
builder.add_node(d)

# 条件判断loop
def route(state:State) -> Literal["b",END]:
    if len(state["aggregate"]) < 7:
        return "b"
    else:
        return END
    
builder.add_edge(START,"a")
builder.add_conditional_edges("a",route)
builder.add_edge("b","c")
builder.add_edge("b","d")
# ["c","d"] 不论c或d谁先开始都到a,简写合并,只能在开始端写,结束端不能
builder.add_edge(["c","d"],"a")


graph = builder.compile()

res = graph.invoke({"aggregate":[]},{"configurable":{"thread_id":"foo"}})
print(res)
