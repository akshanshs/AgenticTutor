from tutor.schemas.state import TutorState
from langgraph.types import interrupt

def teach_lesson(state: TutorState):
    skill = state["current_skill"]
    lesson = state["current_lesson"]
    lesson_graph = state.get("current_lesson_graph", "")

    interrupt(
        {
            "kind": "student_lesson",
            "skill": skill,
            "lesson": lesson,
            "lesson_graph": lesson_graph,

        }
    )

    return {
        "total_lessons": state["total_lessons"] + 1
    }
