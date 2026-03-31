from tutor.schemas.state import TutorState
from tutor.schemas.outputs import DiagnosisOut
from tutor.retrieval.context import answer_context, careless_context, misconcept_context
from tutor.models import llm

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert in analyzing the learners state.
Your job is to analyze one learner response and classify the learner state.
Return structured output with exactly these fields:
Diagnosis:
  - misconception
  - careless_mistake
  - weak_prerequisite
  - good_progress

- reason: a brief explanation of why this diagnosis fits well

Core task:
- Use the learner's answer, the correct answer, the feedback, the lesson context.
- Identify the most likely reason for the learner's performance.
- Choose exactly one diagnosis.

Diagnosis rules:
- good_progress:
  Use this only when the learner's answer is correct.
- careless_mistake:
  Use this when the learner likely knows the concept but made a slip, rushed, misread, or selected the wrong option by accident. Use context dexcribing careless mistakes.
- misconception:
  Use this when the learner's answer suggests an incorrect mental model, false belief, or wrong concept understanding. Use context describing usual misconception context.
- weak_prerequisite:
  Use this when the learner's error suggests they are missing earlier knowledge.

Reasoning rules:
- Base the diagnosis on evidence from the given question and answer. and usefull context.
- Use the context only as support, not as a source of speculation.
- Prefer the most specific diagnosis supported by evidence.

Output rules:
- diagnosis must be exactly one allowed label.
- reason must be concise, specific, and learner-centered.
- Do not add extra fields.
- Do not include chain-of-thought.
        """.strip(),
    ),
    (
        "human",
        """
Analyze this learner's result.

Skill: {skill}
Question: {question}
Student answer: {answer}
Correct answer: {correct_answer}
Score: {score}
Feedback: {feedback}

Concept context:
{concept_prompt}

Misconception context:
{misconcept_prompt}

Carelessness context:
{careless_prompt}
        """.strip(),
    ),
])

chain = prompt | llm.with_structured_output(DiagnosisOut)

def diagnose(state: TutorState):

    concept_prompt = answer_context(state)
    misconcept_prompt = ""
    careless_prompt = ""
    # misconcept_prompt = misconcept_context(state)
    # careless_prompt = careless_context(state)

    result = chain.invoke({
        "skill": state['current_skill'],
        "question": state['current_question'],
        "answer": state['last_answer'],
        "correct_answer": state['correct_last_answer'],
        "score": state['score'],
        "feedback": state['feedback'],
        "concept_prompt": concept_prompt,
        "misconcept_prompt": misconcept_prompt,
        "careless_prompt": careless_prompt
    })

    return {
        "diagnosis": result.diagnosis,
    } 