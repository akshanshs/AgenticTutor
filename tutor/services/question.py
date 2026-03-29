from tutor.schemas.state import TutorState
from langgraph.types import interrupt

def ask_question(state: TutorState):
    skill = state["current_skill"]
    mastery = state["mastery"][skill]
    support = state.get("tool_context") or ""

    learner_answer = interrupt(
        {
            "kind": "student_answer",
            "question": state['current_question'],
            "options": state['current_options'],
            "skill": skill,
            "support_context": support,
            "mastery": mastery,
        }
    )

    return {
        "current_question": state['current_question'],
        "current_options": state['current_options'],
        "correct_last_answer": state["correct_last_answer"],
        "last_answer": learner_answer,
        "tool_context": None,  # consume tool context once used
    }