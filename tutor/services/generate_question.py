from tutor.schemas.state import TutorState
from tutor.schemas.outputs import QuestionOut
from langgraph.types import interrupt
from tutor.retrieval.context import question_context
from tutor.models import llm

import random
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are an adaptive physics tutor.

Create ONE learner-facing question for physics of: {skill}.
at difficulty level: {mastery}*10. On the scale of 0 to 10. With 0 meaning no experience and 10 meaning extremely difficult.
Use the lesson content: {context_prompt}

Optional support context:
{support}

Return:
- One question
- 3 answer options
- Correct answer

Rules for question:
- Keep it brief.
- Ask only one thing.
- Do not include the answer in question.
- Make sure the question is not in {correctly_answered_questions}

Rules for 3 answer_options
- Provide exactly one correct option
- two incorrect but plausible option.
- Shuffle the order of the answer_options.
- The correct option could be 1st or 2nd or 3rd, keep it random

Rules for correct answer
- It should be one of the three answer_options
""")

chain = prompt | llm.with_structured_output(QuestionOut)

def generate_question(state: TutorState):
    skill = state["current_skill"]
    mastery = state["mastery"][skill]
    support = state.get("tool_context") or ""

    is_correct = state.get("is_correct", True)

    if not is_correct:

        return {
            "current_question": state['current_question'],
            "current_options": state['current_options'],
            "correct_last_answer": state["correct_last_answer"],
            #"tool_context": None,  # consume tool context once used
        }

    else:

        context_prompt = question_context(state)
        correctly_answered_questions = state["answered_questions"]

        #question_and_answer = llm.invoke(prompt).content.strip()
        question_and_answer = chain.invoke({
            "skill": skill,
            "mastery": mastery,
            "context_prompt": context_prompt,
            "support": support,
            "correctly_answered_questions": correctly_answered_questions,
        })

        random.shuffle(question_and_answer.answer_options)

        return {
            "current_question": question_and_answer.question,
            "current_options": question_and_answer.answer_options,
            "correct_last_answer": question_and_answer.correct_answer,
            #"tool_context": None,  # consume tool context once used
        }