"""Support assist package with Zepto policy documents."""

from pathlib import Path

from .support import SupportAssistant

DOCS_DIR = Path(__file__).resolve().parent / "docs"
POLICY_DOCS = [
    "doc_01.txt",
    "doc_02.txt",
    "doc_03.txt",
    "doc_04.txt",
    "doc_05.txt",
    "doc_06.txt",
    "doc_07.txt",
    "doc_08.txt",
]


def list_policy_docs():
    """Return the available Zepto policy document filenames."""
    return list(POLICY_DOCS)


def load_policy_doc(doc_name: str) -> str:
    """Read one policy document by filename."""
    doc_path = DOCS_DIR / doc_name
    if not doc_path.exists():
        raise FileNotFoundError(f"Policy document not found: {doc_name}")
    return doc_path.read_text(encoding="utf-8")


__all__ = [
    "SupportAssistant",
    "DOCS_DIR",
    "POLICY_DOCS",
    "list_policy_docs",
    "load_policy_doc",
]
