from tutor.schemas.state import TutorState
from langchain_core.messages import AIMessage, ToolMessage


def queue_tool_call(state: TutorState):
    action_to_tool = {
        "provide_prerequisite_information": "get_prerequisite_note",
        "provide_worked_example": "get_worked_example",
        "provide_hint": "get_targeted_hint",
    }

    tool_name = action_to_tool[state["next_action"]]

    ai_msg = AIMessage(
        content=f"Calling tool {tool_name} for skill {state['current_skill']}",
        tool_calls=[
            {
                "name": tool_name,
                "args": {},
                "id": "tool_call_1",
                "type": "tool_call",
            }
        ],
    )

    return {
        "selected_tool": tool_name,
        "messages": [ai_msg],
    }

def apply_tool_result(state: TutorState):
    # Get the latest ToolMessage
    last_tool_message = None
    for msg in reversed(state["messages"]):
        if isinstance(msg, ToolMessage):
            last_tool_message = msg
            break

    tool_text = last_tool_message.content if last_tool_message else ""

    return {
        "tool_context": tool_text,
        "next_action": "ask_question",
    }