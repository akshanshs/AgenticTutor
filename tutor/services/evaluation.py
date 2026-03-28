from tutor.schemas.state import TutorState
from tutor.schemas.outputs import EvalOut
from tutor.retrieval.context import answer_context
from tutor.models import llm_eval
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are a polite and friendly physics grading expert.

Skill: {current_skill}
Question: {current_question}
Correct answer: {correct_last_answer}
Learner answer: {last_answer}

Return:
- score between 0 and 1
- brief feedback
- whether answer is correct

Rules for feedback:
- if answer is correct, explain why it is correct; you can use this extra information: {context_prompt}
- if answer is wrong, mention it politely
- provide feedback in 15 words
- do not tell the correct answer if the learner is wrong
""")

chain = prompt | llm_eval.with_structured_output(EvalOut)

def evaluate_answer(state: TutorState):

    context_prompt = answer_context(state)

    result = chain.invoke({
        "current_skill": state["current_skill"],
        "current_question": state["current_question"],
        "correct_last_answer": state["correct_last_answer"],
        "last_answer": state["last_answer"],
        "context_prompt": context_prompt,
    })

    return {
        "score": float(result.score),
        "feedback": result.feedback,
        "is_correct": result.is_correct,
        "answered_questions": [state["current_question"]] if result.is_correct else [],
    }