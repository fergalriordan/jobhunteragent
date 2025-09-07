import subprocess

def convert_to_pdf(path_to_word_doc: str, path_to_output_pdf: str) -> bool: 
    """Convert Word doc to PDF using docx2pdf CLI"""
    try:
        subprocess.run(["docx2pdf", path_to_word_doc, path_to_output_pdf], check=True)
        return True
    except Exception:
        return False
