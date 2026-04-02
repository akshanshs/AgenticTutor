from tutor.schemas.state import TutorState
from langgraph.types import interrupt

def teach_lesson(state: TutorState):
    skill = state["current_skill"]
    lesson = state["current_lesson"]

    interrupt(
        {
            "kind": "student_lesson",
            "skill": skill,
            "lesson": lesson,

        }
    )

    return {
        "total_lessons": state["total_lessons"] + 1
    }
