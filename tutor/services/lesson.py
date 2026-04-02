from tutor.schemas.state import TutorState
from langgraph.types import interrupt

def teach_lesson(state: TutorState):
    skill = state["current_skill"]
    lesson = state["current_lesson"]
    skill_answered_questions = dict(state["skill_answered_questions"])
    skill_answered_questions[skill] = 0
    interrupt(
        {
            "kind": "student_lesson",
            "skill": skill,
            "lesson": lesson,

        }
    )

    return {
        "total_lessons": state["total_lessons"] + 1,
        "skill_answered_questions": skill_answered_questions
    }