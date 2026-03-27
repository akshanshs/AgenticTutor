from typing import TypedDict, Optional, Literal, Annotated
from langchain_core.messages import AnyMessage, AIMessage, ToolMessage, HumanMessage
import operator
from langgraph.graph.message import add_messages

# Shared State
class TutorState(TypedDict):
    student_id: str
    mastery: dict[str, float]

    current_skill: str
    current_question: str
    current_options: list[str]
    correct_last_answer: str
    last_answer: str

    score: Optional[float]
    is_correct: Optional[bool]
    feedback: Optional[str]
    diagnosis: Optional[str]

    next_action: Optional[str]
    decision_reason: Optional[str]

    selected_tool: Optional[str]
    tool_context: Optional[str]

    needs_human_review: bool
    teacher_decision: Optional[str]

    question_count: int
    answered_questions: Annotated[list[str], operator.add]
    # Needed for ToolNode
    messages: Annotated[list[AnyMessage], add_messages]
