from tutor.schemas.state import TutorState

def load_student(state: TutorState):
    return state


def choose_skill(state: TutorState):
    weakest = min(state["mastery"], key=state["mastery"].get)
    return {"current_skill": weakest}