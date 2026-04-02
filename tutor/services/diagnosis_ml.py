from tutor.schemas.state import TutorState
from tutor.schemas.outputs import MlFeatures
from tutor.retrieval.context import answer_context, careless_context, misconcept_context
from tutor.models import llm

from langchain_core.prompts import ChatPromptTemplate
import requests

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert in analyzing the learners state.
Your job is to analyze one learner response and extract the information
usefull for machine learning model.
Return structured output with exactly these fields:
Features:
  - cat_1
  - cat_2
  - num_1
  - num_2
Core task:
- Use the learner's answer, the correct answer, the feedback, the lesson context.
Features extraction rules:
- cat_1:
  Use context describing cat_1.
- cat_2:
  Use context describing cat_2.
- num_1:
  Use context describing num_1.
- num_2:
  Use context describing num_2.

rules:
- Base the output on evidence from the given question, answer and feedback. and usefull context about feilds.
- Do not speculate, base your output on information provided by user.
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

chain = prompt | llm.with_structured_output(MlFeatures)

def diagnose_ml(state: TutorState):

    concept_prompt = answer_context(state)
    misconcept_prompt = misconcept_context(state)
    careless_prompt = careless_context(state)

    end_point = "https://azure-function-endpoint" # enfpoint for classification machine learning pipeline on azure cloud

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

    features = {
        "cat_1": result.cat_1,
        "cat_2": result.cat_2,
        "num_1": result.num_1,
        "num_2": result.num_2,
    }

    response = requests.post(end_point, json=features)
    diagnosis = response.json().get("diagnosis") 

    return {
        "diagnosis": diagnosis,
    }