import uuid
import streamlit as st
from langgraph.types import Command

from dotenv import load_dotenv
load_dotenv(override=True)

from tutor.builder import graph

st.set_page_config(page_title="mock test", layout="wide")
st.title("mock test")


# -------------------------
# Defaults
# -------------------------
DEFAULT_MASTERY = {
    "motion": 0.20,
    "force": 0.20,
    "energy": 0.20,
    "thermodynamics": 0.20,
}

OVERRIDE_ACTIONS = [
    "ask_next_question",
    "provide_prerequisite_information",
    "provide_worked_example",
    "provide_hint",
    "end_session",
]


# -------------------------
# Session state init
# -------------------------
def init_session_state():
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if "started" not in st.session_state:
        st.session_state.started = False

    if "history" not in st.session_state:
        st.session_state.history = []

    if "student_id" not in st.session_state:
        st.session_state.student_id = "s1"


init_session_state()


# -------------------------
# Helpers
# -------------------------
def graph_config():
    return {"configurable": {"thread_id": st.session_state.thread_id}}


def build_initial_state(student_id: str, mastery: dict[str, float], learning_rates: dict[str, float], skill_answered_questions: dict[str, int]):
    return {
        "student_id": student_id,
        "mastery": mastery,
        "learning_rates": learning_rates,
        "skill_answered_questions": skill_answered_questions,
        "current_skill": "",
        "current_lesson": "",
        "total_lessons": 0,
        "current_question": "",
        "correct_last_answer": "",
        "last_answer": "",
        "score": None,
        "feedback": None,
        "diagnosis": None,
        "next_action": None,
        "decision_reason": None,
        "selected_tool": None,
        "tool_context": None,
        "needs_human_review": False,
        "teacher_decision": None,
        "answer_count": 0,
        "question_count": 0,
        "answered_questions": [],
        "messages": [],
    }


def get_snapshot():
    return graph.get_state(graph_config())


def get_state_values():
    snapshot = get_snapshot()
    return snapshot.values if snapshot and snapshot.values else {}


def get_interrupt_payload():
    snapshot = get_snapshot()
    interrupts = getattr(snapshot, "interrupts", None) or []
    if not interrupts:
        return None

    first_interrupt = interrupts[0]
    return getattr(first_interrupt, "value", first_interrupt)


def session_finished():
    snapshot = get_snapshot()
    interrupts = getattr(snapshot, "interrupts", None) or []
    nxt = getattr(snapshot, "next", None)
    return not interrupts and not nxt


def start_session(student_id: str, mastery: dict[str, float], learning_rates: dict[str, float], skill_answered_questions: dict[str, int]):
    initial_state = build_initial_state(student_id, mastery, learning_rates, skill_answered_questions)
    graph.invoke(initial_state, config=graph_config())
    st.session_state.started = True
    st.session_state.history = []


def reset_session():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.started = False
    st.session_state.history = []

def resume_student_lesson(lesson: str):

    graph.invoke(Command(resume=lesson), config=graph_config())

def resume_student_answer(answer: str):
    payload = get_interrupt_payload()

    if payload:
        st.session_state.history.append(
            {
                "question": payload.get("question", ""),
                "options": payload.get("options", []),
                "selected_answer": answer,
                "support_context": payload.get("support_context", ""),
                "skill": payload.get("skill", ""),
            }
        )

    graph.invoke(Command(resume=answer), config=graph_config())

    values = get_state_values()
    if st.session_state.history:
        st.session_state.history[-1].update(
            {
                "feedback": values.get("feedback"),
                "score": values.get("score"),
                "diagnosis": values.get("diagnosis"),
                "correct_answer": values.get("correct_last_answer"),
                "decision_reason": values.get("decision_reason"),
                "teacher_decision": values.get("teacher_decision"),
            }
        )


def resume_teacher_decision(mode: str, action: str | None = None):
    decision = {"mode": mode}
    if mode == "override" and action:
        decision["action"] = action

    graph.invoke(Command(resume=decision), config=graph_config())


# -------------------------
# Sidebar controls
# -------------------------
with st.sidebar:
    st.header("Session Setup")

    student_id = st.text_input("Student ID", value=st.session_state.student_id)
    st.session_state.student_id = student_id

    st.subheader("Initial mastery")
    motion = st.slider("Motion", 0.0, 1.0, DEFAULT_MASTERY["motion"], 0.05)
    force = st.slider("Force", 0.0, 1.0, DEFAULT_MASTERY["force"], 0.05)
    energy = st.slider("Energy", 0.0, 1.0, DEFAULT_MASTERY["energy"], 0.05)
    thermo = st.slider("Thermodynamics", 0.0, 1.0, DEFAULT_MASTERY["thermodynamics"], 0.05)

    mastery_input = {
        "motion": motion,
        "force": force,
        "energy": energy,
        "thermodynamics": thermo,
    }

    learning_rates_input = {
        "motion": 0.15,
        "force": 0.15,
        "energy": 0.15,
        "thermodynamics": 0.15,
    }

    skill_answered_questions_input = {
        "motion": 0,
        "force": 0,
        "energy": 0,
        "thermodynamics": 0,
    }

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Start / Restart", use_container_width=True):
            reset_session()
            start_session(student_id, mastery_input, learning_rates_input, skill_answered_questions_input)
            st.rerun()

    with c2:
        if st.button("New Thread", use_container_width=True):
            reset_session()
            st.rerun()

    if st.session_state.started:
        st.caption(f"Thread ID: {st.session_state.thread_id}")


# -------------------------
# Main UI
# -------------------------
if not st.session_state.started:
    st.info("Set the student and mastery values in the sidebar, then click Start / Restart.")
    st.stop()

values = get_state_values()
payload = get_interrupt_payload()

# Top status
c1, c2, c3, c4 = st.columns(4)

current_skill = values.get("current_skill", "-") or "-"
diagnosis = values.get("diagnosis", "-") or "-"

mastery_value = None
if current_skill and values.get("mastery"):
    mastery_value = values["mastery"].get(current_skill)

with c1:
    st.markdown("**Current skill**")
    st.write(current_skill)

with c2:
    st.markdown("**Skill mastery**")
    st.write("-" if mastery_value is None else f"{mastery_value:.2f}")

with c3:
    st.markdown("**Questions answered**")
    st.write(values.get("question_count", 0))

with c4:
    st.markdown("**Diagnosis**")
    st.write(diagnosis)

# Latest feedback
if values.get("feedback"):
    st.subheader("Latest feedback")
    #st.success(values["feedback"]) if (values.get("score") or 0) > 0 else st.warning(values["feedback"])
    if values.get("feedback"):
        #st.subheader("Latest feedback")

        if (values.get("score") or 0) > 0:
            st.success(values["feedback"])
        else:
            st.warning(values["feedback"])
if values.get("decision_reason"):
    st.caption(f"Decision reason: {values['decision_reason']}")

if values.get("teacher_decision"):
    st.caption(f"Teacher decision: {values['teacher_decision']}")

# Finished
if session_finished():
    st.success("Session ended.")
    st.subheader("Final mastery")
    st.json(values.get("mastery", {}))
    st.stop()

# Interrupt handling
if payload and payload.get("kind") == "student_answer":
    st.subheader("Question")

    if payload.get("support_context"):
        st.info(payload["support_context"])

    st.write(payload.get("question", ""))

    form_key = f"student_form_{values.get('question_count', 0)}_{payload.get('question', '')}"
    with st.form(form_key):
        answer = st.radio(
            "Choose one answer",
            payload.get("options", []),
            key=f"radio_{form_key}",
        )
        submitted = st.form_submit_button("Submit answer")

    if submitted:
        resume_student_answer(answer)
        st.rerun()

elif payload and payload.get("kind") == "teacher_review":
    st.subheader("Teacher review required")
    st.warning("The graph requested human review before continuing.")

    left, right = st.columns([1, 1])

    with left:
        st.write(f"**Recommended action:** {payload.get('recommended_action', '-')}")
        st.write(f"**Diagnosis:** {payload.get('diagnosis', '-')}")
        st.write(f"**Skill:** {payload.get('skill', '-')}")
        mastery = payload.get("mastery")
        st.write(f"**Mastery:** {mastery:.2f}" if isinstance(mastery, (int, float)) else "**Mastery:** -")
        st.write(f"**Feedback:** {payload.get('feedback', '-')}")

    with right:
        st.write("**Reason**")
        st.write(payload.get("reason", "-"))

        mode = st.radio(
            "Teacher choice",
            ["approve", "override"],
            horizontal=True,
            key="teacher_mode",
        )

        override_action = None
        if mode == "override":
            override_action = st.selectbox(
                "Override action",
                OVERRIDE_ACTIONS,
                index=0,
                key="override_action",
            )

        if st.button("Send teacher decision"):
            resume_teacher_decision(mode=mode, action=override_action)
            st.rerun()

elif payload and payload.get("kind") == "student_lesson":
    st.subheader("Lesson")

    if payload.get("lesson"):
        st.info(payload["lesson"])

    st.write(payload.get("lesson", ""))

    form_key = f"student_form_{values.get('question_count', 0)}_{payload.get('question', '')}"
    with st.form(form_key):
        answer = st.radio(
            "Click next to continue",
            payload.get("lesson", ""),
            key=f"radio_{form_key}",
        )

        submitted = st.form_submit_button("Next")

    if submitted:
        resume_student_lesson(answer)
        st.rerun()

else:
    st.info("Graph is running or waiting for the next step.")


# -------------------------
# Session history
# -------------------------
if st.session_state.history:
    st.subheader("Session history")

    for i, item in enumerate(reversed(st.session_state.history), start=1):
        title = item.get("question", f"Question {i}")
        with st.expander(title, expanded=False):
            st.write(f"**Skill:** {item.get('skill', '-')}")
            if item.get("support_context"):
                st.write(f"**Support:** {item['support_context']}")
            st.write(f"**Student answer:** {item.get('selected_answer', '-')}")
            if item.get("feedback") is not None:
                st.write(f"**Feedback:** {item.get('feedback')}")
            if item.get("score") is not None:
                st.write(f"**Score:** {item.get('score')}")
            if item.get("diagnosis") is not None:
                st.write(f"**Diagnosis:** {item.get('diagnosis')}")
            if item.get("correct_answer"):
                st.write(f"**Correct answer:** {item.get('correct_answer')}")