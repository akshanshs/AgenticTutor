from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

from tutor.schemas.state import TutorState

from tutor.services.learning_rate import update_learning_rate
from tutor.services.generate_question import generate_question
from tutor.services.question import ask_question
from tutor.services.evaluation import evaluate_answer
from tutor.services.mastery import update_mastery
from tutor.services.diagnosis import diagnose
from tutor.services.decision import decide_next_action
from tutor.services.human_loop import human_review

from tutor.routers import route_after_human_review, route_after_decision
from tutor.tools.application import queue_tool_call, apply_tool_result
from tutor.tools.support_tools import tool_node
from tutor.utils.helpers import load_student, choose_skill

load_dotenv(override=True)

builder = StateGraph(TutorState)

builder.add_node("load_student", load_student)
builder.add_node("choose_skill", choose_skill)
builder.add_node("update_learning_rate", update_learning_rate)
builder.add_node("generate_question", generate_question)
builder.add_node("ask_question", ask_question)
builder.add_node("evaluate_answer", evaluate_answer)
builder.add_node("update_mastery", update_mastery)
builder.add_node("diagnose", diagnose)
builder.add_node("decide_next_action", decide_next_action)
builder.add_node("human_review", human_review)
builder.add_node("queue_tool_call", queue_tool_call)
builder.add_node("tools", tool_node)
builder.add_node("apply_tool_result", apply_tool_result)

builder.add_edge(START, "load_student")
builder.add_edge("load_student", "choose_skill")
builder.add_edge("choose_skill", "update_learning_rate")
builder.add_edge("update_learning_rate", "generate_question")
builder.add_edge("generate_question", "ask_question")
builder.add_edge("ask_question", "evaluate_answer")
builder.add_edge("evaluate_answer", "update_mastery")
builder.add_edge("update_mastery", "diagnose")
builder.add_edge("diagnose", "decide_next_action")

builder.add_conditional_edges(
    "decide_next_action",
    route_after_decision,
    {
        "ask_question": "update_learning_rate",
        "use_prerequisite_tool": "queue_tool_call",
        "use_example_tool": "queue_tool_call",
        "use_hint_tool": "queue_tool_call",
        "end_session": END,
        "human_review": "human_review",
    },
)

builder.add_conditional_edges(
    "human_review",
    route_after_human_review,
    {
        "ask_question": "update_learning_rate",
        "use_prerequisite_tool": "queue_tool_call",
        "use_example_tool": "queue_tool_call",
        "use_hint_tool": "queue_tool_call",
        "end_session": END,
    },
)

builder.add_edge("queue_tool_call", "tools")
builder.add_edge("tools", "apply_tool_result")
builder.add_edge("apply_tool_result", "generate_question")

graph = builder.compile(checkpointer=InMemorySaver())