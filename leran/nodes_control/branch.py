import operator
from typing import Annotated,Any
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

# branch START -> a |->b ->| -> d ->END
#                   |->c ->|
builder.add_edge(START,"a")
builder.add_edge("a","b")
builder.add_edge("a","c")
builder.add_edge("b","d")
builder.add_edge("c","d")
builder.add_edge("d",END)

graph = builder.compile()

res = graph.invoke({"aggregate":[]},{"configurable":{"thread_id":"foo"}})
print(res)
