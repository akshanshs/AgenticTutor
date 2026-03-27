from langchain.tools import tool, ToolRuntime
from langgraph.prebuilt import ToolNode

from tutor.models import llm

@tool
def get_prerequisite_note(runtime: ToolRuntime) -> str:
    """Return a short prerequisite refresher for a skill."""

    state = runtime.state
    question = state['current_question']
    answer = state['correct_last_answer']
    student_answer = state['last_answer']

    prompt = f"""
    Question: {question}
    Correct answer: {answer}
    student's answer: {student_answer}

    provide the name of
    two pre requisite concept.

    Rules
    - 1 concept should be from Mathematics
    - 1 concepts shpuld be from Physics
    - Do not list the concept of the current question
    """.strip()

    prerequisite = llm.invoke(prompt).content

    return f"Please review the concepts: {prerequisite}"

@tool
def get_worked_example(runtime: ToolRuntime) -> str:
    """Return one tiny worked example for a skill."""
    state = runtime.state
    question = state['current_question']
    answer = state['correct_last_answer']
    student_answer = state['last_answer']

    prompt = f"""
    Question: {question}
    Correct answer: {answer}
    student's answer: {student_answer}

    Provide a simplest worked example
    for the {question}
    Rules
    - Do not use latex, only markdown text
    """.strip()

    example = llm.invoke(prompt).content
    return f"Worked example for {example}"

@tool
def get_targeted_hint(runtime: ToolRuntime) -> str:
    """Return one short hint for a skill."""
    state = runtime.state
    question = state['current_question']
    answer = state['correct_last_answer']
    student_answer = state['last_answer']

    prompt = f"""
    Question: {question}
    Correct answer: {answer}
    student's answer: {student_answer}

    Provide a hint for the student
    depending on the reason of incorrent answer.
    rules
    - Do not use latex. Provide onlt markdown text
    """.strip()

    hint = llm.invoke(prompt).content

    return f"Try understand {hint}"

TOOLS = [get_prerequisite_note, get_worked_example, get_targeted_hint]
tool_node = ToolNode(TOOLS)