from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
llm_eval = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)