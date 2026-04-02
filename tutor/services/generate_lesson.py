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
- between 30 and 40 words
- based only on the provided lesson context
- cover the central concepts needed to understand the target skill
- avoid numerical calculations and worked examples
- avoid repetition

Also create a concept graph in Graphviz DOT format.
Graph rules:
- use `digraph Lesson { ... }`
- include 3 to 6 short concept nodes
- directed edges should represent "supports", "causes", or "leads to" relationships
- keep labels short and beginner friendly
- return valid DOT syntax only
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
        "current_lesson_graph": lesson.lesson_graph,
    }
