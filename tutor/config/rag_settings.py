from dataclasses import dataclass

@dataclass(frozen=True)
class RagConfig:
    persist_dir: str
    collection_name: str
    embedding_model: str
    k: int = 4


question_rag = RagConfig(
    persist_dir="vector_db/vector_physics",
    collection_name="physics_book",
    embedding_model="text-embedding-3-small",
    k=4,
)

answer_rag = RagConfig(
    persist_dir="vector_db/vector_physics",
    collection_name="physics_book",
    embedding_model="text-embedding-3-small",
    k=4,
)

misconcept_rag = RagConfig(
    persist_dir="vector_db/vector_misconcepts",
    collection_name="misconception",
    embedding_model="text-embedding-3-small",
    k=4,
)

careless_rag = RagConfig(
    persist_dir="vector_db/vector_careless",
    collection_name="careless_mistakes",
    embedding_model="text-embedding-3-small",
    k=4,
)