import os
from pathlib import Path

project_name = "tutor"

list_of_files = [
    "app.py",

    "scripts/build_vector_store.py",
    "scripts/seed_data.py",

    "vector_db/.gitkeep",

    f"{project_name}/__init__.py",

    f"{project_name}/config/__init__.py",
    f"{project_name}/config/rag_settings.py",

    # f"{project_name}/constants/__init__.py",
    # f"{project_name}/constants/skills.py",

    f"{project_name}/schemas/__init__.py",
    f"{project_name}/schemas/state.py",
    f"{project_name}/schemas/outputs.py",

    f"{project_name}/retrieval/__init__.py",
    f"{project_name}/retrieval/chroma_store.py",

    f"{project_name}/services/__init__.py",
    f"{project_name}/services/question.py",
    f"{project_name}/services/evaluation.py",
    f"{project_name}/services/diagnosis.py",
    f"{project_name}/services/mastery.py",
    f"{project_name}/services/decision.py",
    f"{project_name}/services/learning_rate.py",
    f"{project_name}/services/learning_path.py",

    f"{project_name}/tools/__init__.py",
    f"{project_name}/tools/support_tools.py",

    f"{project_name}/router.py",
    f"{project_name}/builder.py",

    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/helpers.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w", encoding="utf-8") as f:
            pass
    else:
        print(f"file already exists: {filepath}")