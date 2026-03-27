from tutor.config.rag_settings import answer_rag, question_rag
from tutor.retrieval.chroma_store import get_vectordb
from tutor.schemas.state import TutorState

def question_context(state: TutorState) -> str:

    vectordb = get_vectordb(question_rag)

    skill = state['current_skill']
    mastery = state["mastery"][skill]
    window = 1

    all_docs = vectordb.get(
        where={"lesson": skill},
        include=["documents", "metadatas"]
    )

    pages = sorted({
        m["page"] for m in all_docs["metadatas"] if m is not None and "page" in m
    })
    start_page, end_page = min(pages), max(pages)
    target_page = round(start_page + (end_page - start_page) * mastery)
    page_from = max(start_page, (target_page - window))
    page_to = min(end_page, (target_page + window))

    docs = vectordb.get(
        where={
            "$and": [
                {"lesson": skill},
                {"page": {"$gte": page_from}},
                {"page": {"$lte": page_to}}
            ]
        },
        include=["documents", "metadatas"]
    )

    pairs = sorted(
        zip(docs["metadatas"], docs["documents"]),
        key=lambda x: (x[0]["page"], x[0].get("chunk", 0))
    ) 

    context_prompt = "\n\n".join(doc for _, doc in pairs)
    return context_prompt



def answer_context(state: TutorState) -> str:

    vectordb = get_vectordb(answer_rag)

    skill = state["current_skill"]
    question = state["current_question"]
    correct_answer = state["correct_last_answer"]

    query = f"""
    Skill: {skill}
    Question: {question}
    Correct answer: {correct_answer}
    """.strip()

    docs = vectordb.similarity_search(
        query=query,
        k=4,
        filter={"lesson": skill}
    )

    context_prompt = "\n\n".join(doc.page_content for doc in docs)
    return context_prompt