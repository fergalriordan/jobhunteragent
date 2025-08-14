from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def load_cv_info() -> str: 
    """Load CV information from text file"""
    with open("cv.txt") as f:
        cv = f.read()
    
    return cv