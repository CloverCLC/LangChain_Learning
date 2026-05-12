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


builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)

# 条件判断loop
def route(state:State) -> Literal["b",END]:
    if len(state["aggregate"]) < 7:
        return "b"
    else:
        return END
    
builder.add_edge(START,"a")
builder.add_conditional_edges("a",route)
builder.add_edge("b","a")


graph = builder.compile()

# res = graph.invoke({"aggregate":[]},{"configurable":{"thread_id":"foo"}})
# print(res)


# 通过添加 recursion_limit 参数限制 loop 次数
from langgraph.errors import GraphRecursionError
try:
    graph.invoke({"aggregate":[]},{"recursion_limit":4})
except GraphRecursionError:
    # Recursion [rɪ'kɜ:ʃn] n.递归
    print("Recursion Error")
