from tutor.schemas.state import TutorState
from tutor.schemas.outputs import DiagnosisOut
from tutor.retrieval.context import answer_context
from tutor.models import llm

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are diagnosing why a student performed this way.

Skill: {skill}
Question: {question}
Student's answer: {answer}
Correct answer: {correct_answer}
Score: {score}
Feedback: {feedback}

If student answer is incorrect, figure out the mistake and find out the reason for the wrong answer.
if needed here is some extra context: {concept_prompt}

Classify the learner state as exactly one of:
- misconception
- careless_mistake
- weak_prerequisite
- good_progress
""")

chain = prompt | llm.with_structured_output(DiagnosisOut)

def diagnose(state: TutorState):

    concept_prompt = answer_context(state)
    # misconcept_prompt = misconcept_context(state)
    # careless_prompt = careless_context(state)

    result = chain.invoke({
        "skill": state['current_skill'],
        "question": state['current_question'],
        "answer": state['last_answer'],
        "correct_answer": state['correct_last_answer'],
        "score": state['score'],
        "feedback": state['feedback'],
        "concept_prompt": concept_prompt
    })

    return {
        "diagnosis": result.diagnosis,
    } 