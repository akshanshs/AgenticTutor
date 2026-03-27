from tutor.schemas.state import TutorState
from tutor.schemas.outputs import DiagnosisOut
from tutor.retrieval.context import answer_context
from tutor.models import llm

def diagnose(state: TutorState):

    concept_prompt = answer_context(state)
    # misconcept_prompt = misconcept_context(state)
    # careless_prompt = careless_context(state)


    prompt = f"""
    You are diagnosing why a student performed this way.

    Skill: {state['current_skill']}
    Question: {state['current_question']}
    Student's answer: {state['last_answer']}
    Correct answer: {state['correct_last_answer']}
    Score: {state['score']}
    Feedback: {state['feedback']}

    If student answer is incorrect, figure out the mistake and find out the reason for the wrong answer.
    if needed here is some extra context: {concept_prompt}

    Classify the learner state as exactly one of:
    - misconception
    - careless_mistake
    - weak_prerequisite
    - good_progress
    """

    result = llm.with_structured_output(DiagnosisOut).invoke(prompt)

    return {
        "diagnosis": result.diagnosis,
    } 