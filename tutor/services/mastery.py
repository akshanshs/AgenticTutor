from tutor.schemas.state import TutorState

def update_mastery(state: TutorState):
    skill = state["current_skill"]
    old = state["mastery"][skill]
    score = state["score"] or 0.0

    # Simple exponential update
    new_value = old + 0.2 * (score - old)

    mastery = dict(state["mastery"])
    mastery[skill] = round(new_value, 3)

    return {
        "mastery": mastery,
        "question_count": state["question_count"] + 1,
    }