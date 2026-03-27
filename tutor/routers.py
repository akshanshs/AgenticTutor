from tutor.schemas.state import TutorState

def route_after_decision(state: TutorState):
    if state["needs_human_review"]:
        return "human_review"
    return state["next_action"]


def route_after_human_review(state: TutorState):
        return state["next_action"]