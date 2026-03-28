from pydantic import BaseModel, Field
from typing import Literal

class QuestionOut(BaseModel):
    question: str = Field(description="The quiz question")
    answer_options: list[str] = Field(min_length=3, max_length=3, description="three possible answer to the question one correct, and another incorrect")
    correct_answer: str = Field(description="The exact text of the correct answer, matching one item in answer_options")

class EvalOut(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    feedback: str = Field(description="explanation for the correct answer")
    is_correct: bool

class LearningOut(BaseModel):
    learning_rate: float = Field(
        description="Rate at which learning proceeds",
        ge=0.05,
        le=0.2
    )

class DiagnosisOut(BaseModel):
    diagnosis: Literal[
        "misconception",
        "careless_mistake",
        "weak_prerequisite",
        "good_progress",
    ]
    reason: str

class DecisionOut(BaseModel):
    action: Literal[
        "ask_question",
        "use_prerequisite_tool",
        "use_example_tool",
        "use_hint_tool",
        "end_session",
    ]
    needs_human_review: bool
    reason: str