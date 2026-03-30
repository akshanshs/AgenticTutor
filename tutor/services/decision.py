from tutor.schemas.state import TutorState
from tutor.schemas.outputs import DecisionOut
from tutor.retrieval.context import decision_context
from tutor.models import llm

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an adaptive physics tutor deciding the next pedagogical action.

Return structured output with exactly:
- next_action: one of ["ask_next_question", "provide_prerequisite_information", "provide_worked_example", "provide_hint"]
- needs_human_review: boolean
- decision_reason: string

Use action Rules and decision policies.

Action rules:
- ask_next_question:
  Use when the learner answered correctly or is showing good_progress.
- provide_prerequisite_information:
  Use when the learner lacks supporting prior knowledge related to mathematics or beginner physics.
- provide_worked_example:
  Use when the learner shows a misconception or careless mistake and would benefit from a clear solution.
- provide_hint:
  Use when the learner made a misconception or careless mistake or seems close to the correct answer.

Important information for Action decision:
- Use the decision policy provided by human.

Human review rules:
- true only for ambiguous or conflicting cases. Unclear or conflicting policies.
Reasoning rules:
- Base the decision primarily on decision policies, correctness, diagnosis, and feedback.
- Use mastery and question_count as secondary context.
- Prefer the least intrusive useful support.
- Choose exactly one action.
- Keep decision_reason brief.
        """.strip(),
    ),
    (
        "human",
        """
Learner case:

Skill: {skill}
Question: {question}
Learner's answer: {answer}
Learner's answers is: {is_correct}
Feedback: {feedback}
Diagnosis: Learner has {diagnosis}
Acation deciding policies: {decision_policy}
        """.strip(),
    ),
])

chain = prompt | llm.with_structured_output(DecisionOut)

def decide_next_action(state: TutorState):
    skill = state["current_skill"]

    # decision_policy = decision_context(state)
    decision_policy = ""

    result = chain.invoke({
        "skill": skill,
        "question": state['current_question'],
        "answer": state['last_answer'],
        "is_correct": state["is_correct"],
        "feedback": state["feedback"],
        "diagnosis": state['diagnosis'],
        "decision_policy": decision_policy
    })

    return {
        "next_action": result.action,
        "decision_reason": result.reason,
        "needs_human_review": bool(result.needs_human_review),
    }