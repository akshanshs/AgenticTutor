from tutor.schemas.state import TutorState
from tutor.schemas.outputs import LearningOut
from tutor.models import llm

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are an adapting tutor and adjust how fast students need to learn.

Skill: {skill}
Learning rate: {learning_rate}
Performance: {performance}

The best performance should be 0.8, no more and no less.
A low learning rate increases performance and a high learning rate decreases performance.
Adjust the learning rate so that the performance can reach 0.8.

Return:
- learning rate between 0.05 and 0.25

Rules for learning rate:
- if performance < 0.8, return a learning rate < {learning_rate}
- if performance > 0.8, return a learning rate > {learning_rate}
""")

chain = prompt | llm.with_structured_output(LearningOut)

def update_learning_rate(state: TutorState):
    skill = state["current_skill"]
    learning_rate = state["learning_rates"][skill] or 0.15
    no_of_questions = state["question_count"] or 1
    no_of_answers = state["answer_count"] or 1

    performance = no_of_answers/no_of_questions

    new_learning_rate = chain.invoke({
        "skill": skill,
        "learning_rate": learning_rate,
        "performance": performance
    })

    learning_rates = dict(state["learning_rates"])
    learning_rates[skill] = round(new_learning_rate.learning_rate, 3)

    return {
        "learning_rates": learning_rates
    }