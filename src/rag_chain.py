from pathlib import Path
from typing import List, Optional

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document

from prompts import SYSTEM_PROMPT, ANSWER_PROMPT  # keep this file alongside app.py

VS_PATH = Path("vectorstore/index")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # must match ingest.py


# --------------------------- Helper: format context ----------------------------- #
def format_context(docs: List[Document]) -> str:
    """
    Convert list of Document objects to formatted string for prompt context.
    Adjust formatting here as needed.
    """
    parts = []
    for i, doc in enumerate(docs):
        parts.append(f"[Document {i+1}]:\n{doc.page_content}\n")
    return "\n---\n".join(parts)


# --------------------------- retrieval ----------------------------- #
def get_docs(question: str, k: int = 4, company_filter: Optional[List[str]] = None):
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = FAISS.load_local(str(VS_PATH), embeddings, allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_kwargs={"k": max(1, k)})

    # If filtering by company, over-fetch to avoid empty results
    fetch_k = max(k * 6, 30) if company_filter else k
    retriever.search_kwargs["k"] = fetch_k

    docs = retriever.get_relevant_documents(question)

    if company_filter:
        wanted = {c.lower() for c in company_filter}
        docs = [d for d in docs if d.metadata.get("company", "").lower() in wanted]
        # if still empty, gracefully fall back to unfiltered top-k so you at least get an answer
        if not docs:
            docs = retriever.get_relevant_documents(question)

    # cap to k results
    return docs[:k]


# ----------------------------- answer ------------------------------ #
def answer_question(question: str, k: int = 4, company_filter: Optional[List[str]] = None) -> dict:
    """
    Returns dict with:
      - 'answer': str (LLM answer or context fallback)
      - 'context_docs': List[Document]
    """
    docs = get_docs(question, k=k, company_filter=company_filter)
    context = format_context(docs)

    try:
        # If you have no OpenAI credits, the except block will show the context instead.
        llm = ChatOpenAI(model="gpt-4o-mini")
        prompt = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_PROMPT), ("human", ANSWER_PROMPT)]
        )
        msg = prompt.format_messages(question=question, context=context)
        resp = llm.invoke(msg)
        answer = resp.content
    except Exception:
        answer = "Model unavailable (likely no API credits). Showing top source snippets instead.\n\n" + context

    return {"answer": answer, "context_docs": docs}
