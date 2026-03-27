from tutor.schemas.state import TutorState
from langgraph.types import interrupt

def human_review(state: TutorState):
    teacher_decision = interrupt(
        {
            "kind": "teacher_review",
            "recommended_action": state["next_action"],
            "reason": state["decision_reason"],
            "diagnosis": state["diagnosis"],
            "skill": state["current_skill"],
            "mastery": state["mastery"][state["current_skill"]],
            "feedback": state["feedback"],
        }
    )

    mode = teacher_decision.get("mode", "approve")

    if mode == "override":
        override_action = teacher_decision["action"]
        return {
            "next_action": override_action,
            "teacher_decision": f"override -> {override_action}",
        }

    return {
        "teacher_decision": "approved",
    }