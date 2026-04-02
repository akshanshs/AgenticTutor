from tutor.schemas.state import TutorState

def route_after_decision(state: TutorState):
    if state["needs_human_review"]:
        return "human_review"
    return state["next_action"]


def route_after_human_review(state: TutorState):
        return state["next_action"]

def route_after_lr_update(state: TutorState):
    skill = state["current_skill"]
    skill_answered_questions = dict(state["skill_answered_questions"])


    if skill_answered_questions[skill] > 2:
        return "new_lesson"
    else:
        return "continue_questioning"