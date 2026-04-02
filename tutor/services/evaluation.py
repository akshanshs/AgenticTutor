from app import skill_answered_questions_input
from tutor.schemas.state import TutorState
from tutor.schemas.outputs import EvalOut
from tutor.retrieval.context import answer_context
from tutor.models import llm_eval
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a polite, friendly, and precise physics grading expert.

Your job is to grade one learner answer for one physics question.

You must return structured output with:
- score: a float between 0 and 1
- feedback: a brief message for the learner
- is_correct: a boolean

Grading rules:
- Mark is_correct as true only if the learner answer matches the correct answer.
- If the learner answer is correct, set score to 1.0.
- If the learner answer is wrong, set score to 0.0.
- Be strict about correctness, but keep the tone encouraging.

Feedback rules:
- Maximum 15 words.
- If the answer is correct, briefly explain why it is correct.
- If the answer is wrong, say it is not correct in a polite way.
- If the answer is wrong, do not reveal the correct answer.
- Use the provided lesson context to make the feedback helpful.
        """.strip(),
    ),
    (
        "human",
        """
Evaluate the learner response.

Skill: {current_skill}
Question: {current_question}
Correct answer: {correct_last_answer}
Learner's answer: {last_answer}

Lesson context:
{context_prompt}
        """.strip(),
    ),
])

chain = prompt | llm_eval.with_structured_output(EvalOut)

def evaluate_answer(state: TutorState):

    context_prompt = answer_context(state)
    skill = state["current_skill"]
    skill_answered_questions = dict(state["skill_answered_questions"])

    result = chain.invoke({
        "current_skill": skill,
        "current_question": state["current_question"],
        "correct_last_answer": state["correct_last_answer"],
        "last_answer": state["last_answer"],
        "context_prompt": context_prompt,
    })

    if result.is_correct:
        answered_count = state["answer_count"] + 1
        skill_answered_questions[skill] = skill_answered_questions[skill] + 1
    else:
        answered_count = state["answer_count"]

    return {
        "score": float(result.score),
        "feedback": result.feedback,
        "is_correct": result.is_correct,
        "answered_questions": [state["current_question"]] if result.is_correct else [],
        "answered_count": answered_count,
        "skill_answered_questions": skill_answered_questions
    }