from tutor.schemas.state import TutorState
from tutor.schemas.outputs import DecisionOut
from tutor.models import llm

def decide_next_action(state: TutorState):
    skill = state["current_skill"]
    mastery = state["mastery"][skill]

    prompt = f"""
    You are an adaptive tutor deciding the next pedagogical action.

    Skill: {skill}
    Mastery: {mastery}, on scale from 0 to 1.
    Question: {state['current_question']}
    Student's answer: {state['last_answer']}
    Evaluation and feedback: {state['feedback']}
    Diagnosis: {state['diagnosis']}
    Question count: {state['question_count']}

    Available actions:
    - ask_question
    - use_prerequisite_tool
    - use_example_tool
    - use_hint_tool
    - end_session

    Choose the single best next action.
    Also set needs_human_review = true if:
    - the case looks ambiguous, or
    - mastery is high but performance suddenly drops, or
    - you are not confident in the intervention.
    """

    result = llm.with_structured_output(DecisionOut).invoke(prompt)

    return {
        "next_action": result.action,
        "decision_reason": result.reason,
        "needs_human_review": bool(result.needs_human_review),
    }