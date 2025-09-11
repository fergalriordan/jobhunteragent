from docx2pdf import convert

def convert_to_pdf(path_to_word_doc: str, path_to_output_pdf: str) -> bool:
    try:
        convert(path_to_word_doc, path_to_output_pdf)
        return True
    except Exception as e:
        print(f"❌ Error converting to PDF: {e}")
        return False
