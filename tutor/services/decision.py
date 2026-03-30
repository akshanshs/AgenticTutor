from tutor.schemas.state import TutorState
from tutor.schemas.outputs import DecisionOut
from tutor.retrieval.context import decision_context
from tutor.models import llm

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are an adaptive tutor deciding the next pedagogical action.

Skill: {skill}
Mastery: {mastery}, on scale from 0 to 1.
Question: {question}
Student's answer: {answer}
Evaluation and feedback: {feedback}
Diagnosis: {diagnosis}
Question count: {question_count}

Available actions:
- ask_question
- use_prerequisite_tool
- use_example_tool
- use_hint_tool

Choose the single best next action.
Also set needs_human_review = true if:
- the case looks ambiguous, or
- mastery is high but performance suddenly drops, or
- you are not confident in the intervention.
""")
# - end_session

chain = prompt | llm.with_structured_output(DecisionOut)

def decide_next_action(state: TutorState):
    skill = state["current_skill"]
    mastery = state["mastery"][skill]

    # decision_policy = decision_context(state)

    result = chain.invoke({
        "skill": skill,
        "mastery": mastery,
        "question": state['current_question'],
        "answer": state['last_answer'],
        "feedback": state["feedback"],
        "diagnosis": state['diagnosis'],
        "question_count": state['question_count'],
    })

    return {
        "next_action": result.action,
        "decision_reason": result.reason,
        "needs_human_review": bool(result.needs_human_review),
    }