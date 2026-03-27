from tutor.schemas.state import TutorState
from tutor.schemas.outputs import QuestionOut
from langgraph.types import interrupt
from tutor.retrieval.context import question_context
from tutor.models import llm

def ask_question(state: TutorState):
    is_correct = state.get("is_correct", True)

    if not is_correct:
        learner_answer = interrupt(
            {
                "kind": "student_answer",
                "question": state['current_question'],
                "options": state['current_options'],
                "skill": skill,
                "support_context": support,
                "mastery": mastery,
            }
        )
    else:
        skill = state["current_skill"]
        mastery = state["mastery"][skill]
        support = state.get("tool_context") or ""

        context_prompt = question_context(state)
        correctly_answered_questions = state["answered_questions"]

        prompt = f"""
        You are an adaptive physics tutor.

        Create ONE learner-facing question for physics of: {skill}.
        at difficulty matching mastery: {mastery}. On the scale of 0 to 1. With 0 meaning no experience and 1 meaning expert.
        Use the lesson content: {context_prompt}

        Optional support context:
        {support}

        Return:
        - One question
        - 2 answer options
        - Correct answer

        Rules for question:
        - Keep it brief.
        - Ask only one thing.
        - Do not include the answer in question.
        - Make sure the question is not in {correctly_answered_questions}

        Rules for 2 answer_options
        - Provide exactly one correct option and one incorrect but plausible option.
        - Shuffle the order of the answer_options.
        - Do not always place the correct answer first.

        Rules for correct answer
        - It should be one of the 2 answer_options
        """

        #question_and_answer = llm.invoke(prompt).content.strip()
        question_and_answer = llm.with_structured_output(QuestionOut, method="json_schema").invoke(prompt)

        learner_answer = interrupt(
            {
                "kind": "student_answer",
                "question": question_and_answer.question,
                "options": question_and_answer.answer_options,
                "skill": skill,
                "support_context": support,
                "mastery": mastery,
            }
        )

    return {
        "current_question": question_and_answer.question,
        "correct_last_answer": question_and_answer.correct_answer,
        "last_answer": learner_answer,
        "tool_context": None,  # consume tool context once used
    }