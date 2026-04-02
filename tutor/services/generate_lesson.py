from tutor.schemas.state import TutorState
from tutor.schemas.outputs import LessonOut
from tutor.retrieval.context import lesson_context
from tutor.models import llm

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a skilled physics tutor creating a summary from lesson content.

Write a short concept-focused lesson for teaching the learner.

Requirements:
- exactly one paragraph
- between 60 and 70 words
- based only on the provided lesson context
- cover the central concepts needed to understand the target skill
- avoid numerical calculations and worked examples
- avoid repetition
        """.strip(),
    ),
    (
        "human",
        """
Please create a physics lesson for.

Skill:
{skill}

Lesson context:
{context_prompt}
        """.strip(),
    ),
])

chain = prompt | llm.with_structured_output(LessonOut)

def generate_lesson(state: TutorState):

    skill = state["current_skill"]
    context_prompt = lesson_context(state)

    lesson = chain.invoke({
        "skill": skill,
        "context_prompt": context_prompt
    })

    return {
        "current_lesson": lesson.lesson,
    }
