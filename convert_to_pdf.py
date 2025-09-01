import subprocess
from langchain_core.tools import tool

@tool
def convert_to_pdf(path_to_word_doc: str) -> bool: 
    """Convert Word doc to PDF using docx2pdf CLI"""
    try:
        subprocess.run(["docx2pdf", path_to_word_doc, "tailored_cv.pdf"], check=True)
        return True
    except Exception:
        return False
