from tutor.schemas.state import TutorState
from tutor.schemas.outputs import LearningOut
from tutor.models import llm

def update_learning_rate(state: TutorState):
    skill = state["current_skill"]
    learning_rate = state["learning_rates"][skill]
    no_of_questions = state["question_count"] or 1
    no_of_answers = state["answer_count"] or 1

    performance = no_of_answers/no_of_questions

    prompt = f"""
    You are a serious adapting tutor and adjust how fast students needs to learn.

    Skill: {skill}
    learning rate: {learning_rate}
    Performance: {performance}

    The best performance should be 0.8, no more no less.
    Low learning rate increases the performance and high learning rate decreases the performance.
    Adjust the learning rate so that the performance can reach 0.8.

    Return:
    - learning rate between 0.05 and 0.25

    Rules for learning rate:
    - if performance < 0.8, return a learning rate < {learning_rate}
    - if performance > 0.8, return a learning rate > {learning_rate}
    """

    new_learning_rate = llm.with_structured_output(LearningOut).invoke(prompt)

    learning_rates = dict(state["learning_rates"])
    learning_rates[skill] = round(new_learning_rate, 3)

    return {
        "learning_rates": learning_rates
    }