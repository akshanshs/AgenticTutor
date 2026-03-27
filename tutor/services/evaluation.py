from tutor.schemas.state import TutorState
from tutor.schemas.outputs import EvalOut
from tutor.retrieval.context import answer_context
from tutor.models import llm_eval

def evaluate_answer(state: TutorState):

    context_prompt = answer_context(state)

    prompt = f"""
    You are a polite and friendly, physics grading expert.

    Skill: {state['current_skill']}
    Question: {state['current_question']}
    Correct answer: {state['correct_last_answer']}
    Learner answer: {state['last_answer']}

    Return:
    - score between 0 and 1
    - brief feedback
    - whether answer is correct

    Rules for feedback:
    - if answer is correct, explanation why answer is correct, you can use the extra infromation: {context_prompt}
    - if answer is wrong. Mention is politely. Provide feedback in 15 words. do not tell the answer.
    """

    result = llm_eval.with_structured_output(EvalOut).invoke(prompt)

    return {
        "score": float(result.score),
        "feedback": result.feedback,
        "is_correct": result.is_correct,
        "answered_questions": [state["current_question"]] if result.is_correct else [],
    }