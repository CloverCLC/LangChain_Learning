# TypedDict 属于python标准库中typing模块的一部分,仅提供静态类型检查
# pydantic 属于第三方库,提供运行时数据验证和序列化功能
from langchain_core.messages import AnyMessage,AIMessage,HumanMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph

# 定义节点间通讯的消息格式
class State(TypedDict):
    messages:list[AnyMessage]
    extra_field:int

# 创建节点(node)
def node(state:State):
    messages = state['messages']
    new_messages = AIMessage("hello,im node1")
    return {
        "messages":messages+[new_messages],
        "extra_field":1
    }

# 创建图(Graph)
graph = StateGraph(State)
graph.add_node(node)
graph.set_entry_point("node")
graph_builder = graph.compile()


result = graph_builder.invoke({
    "messages":[HumanMessage("hello")]
})
# print(result)
for message in result['messages']:
    message.pretty_print()
