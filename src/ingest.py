# src/ingest.py
from pathlib import Path
from typing import List, Tuple
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DOCS_DIR = Path("data/docs")
VS_PATH = Path("vectorstore/index")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # free/local

# ----------------------------- helpers ----------------------------- #
def infer_company(filename_stem: str) -> Tuple[str, str]:
    """Infer company + ticker from the filename."""
    base = filename_stem.lower()
    if "microsoft" in base or "msft" in base:
        return "Microsoft", "MSFT"
    if "amazon" in base or "amzn" in base:
        return "Amazon", "AMZN"
    if "apple" in base or "aapl" in base:
        return "Apple", "AAPL"
    if "meta" in base or "facebook" in base or "meta_platforms" in base or "fb" in base:
        return "Meta", "META"
    if "alphabet" in base or "google" in base or "googl" in base or "goog" in base:
        return "Alphabet", "GOOGL"
    return filename_stem, ""

def load_docs() -> List:
    """Load .pdf and .txt files and attach metadata (company, ticker, source)."""
    docs = []
    for p in sorted(DOCS_DIR.iterdir()):
        if not p.is_file():
            continue

        company, ticker = infer_company(p.stem)

        if p.suffix.lower() == ".pdf":
            loaded = PyPDFLoader(str(p)).load()
        elif p.suffix.lower() in (".txt", ".text"):
            loaded = TextLoader(str(p), encoding="utf-8").load()
        else:
            # skip unknown file types
            continue

        for d in loaded:
            d.metadata = d.metadata or {}
            d.metadata["company"] = company
            if ticker:
                d.metadata["ticker"] = ticker
            d.metadata["source"] = str(p)
        docs.extend(loaded)
    return docs

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,      # a bit larger to reduce total chunks
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)

def build_index(splits):
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = FAISS.from_documents(splits, embeddings)
    VS_PATH.parent.mkdir(parents=True, exist_ok=True)
    vs.save_local(str(VS_PATH))
    print(f"Saved index to {VS_PATH}")

# ------------------------------ main ------------------------------- #
if __name__ == "__main__":
    if not DOCS_DIR.exists():
        raise SystemExit("Folder data/docs not found.")
    docs = load_docs()
    if not docs:
        raise SystemExit("No supported files (.pdf/.txt) in data/docs.")
    splits = split_docs(docs)
    print(f"Loaded {len(docs)} docs → {len(splits)} chunks")
    build_index(splits)
