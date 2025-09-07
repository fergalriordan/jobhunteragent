from typing import Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

# ---- Import tools ----
from tools.generate_tailored_cv import generate_tailored_cv
from tools.convert_to_pdf import convert_to_pdf

# ---- Define state ----
class CVPipelineState(BaseModel):
    job_listing: str
    cv_template: str
    tailored_cv_path: Optional[str] = None
    approved: bool = False
    pdf_path: Optional[str] = None

# ---- Define nodes ----
def generate_cv_node(state: CVPipelineState):
    """Generate tailored CV (docx)."""
    output_path = "outputs/tailored_cv.docx"
    try:
        generate_tailored_cv(
            path_to_job_listing=state.job_listing,
            path_to_projects_info="inputs/user_details/projects.txt",
            path_to_response_format="inputs/cv_template/response_format.txt",
            path_to_cv_template=state.cv_template,
            path_to_output_cv=output_path,
        )
        state.tailored_cv_path = output_path
        print(f"✅ Tailored CV generated: {output_path}")
    except Exception as e:
        print(f"❌ Error generating CV: {e}")
        state.tailored_cv_path = None
    return state

def approval_node(state: CVPipelineState):
    """Simple human-in-the-loop approval."""
    print(f"\nGenerated CV: {state.tailored_cv_path}")
    response = input("Do you approve this CV? (y/n): ").strip().lower()
    state.approved = (response == "y")
    return state

def convert_pdf_node(state: CVPipelineState):
    """Convert CV to PDF if approved."""
    if state.approved:
        pdf_path = state.tailored_cv_path.replace(".docx", ".pdf")
        try:
            convert_to_pdf(state.tailored_cv_path, pdf_path)
            state.pdf_path = pdf_path
            print(f"✅ CV converted to PDF: {pdf_path}")
        except Exception as e:
            print(f"❌ Error converting to PDF: {e}")
    else:
        print("❌ CV not approved. Skipping PDF conversion.")
    return state

# ---- Build LangGraph workflow ----
workflow = StateGraph(state_schema=CVPipelineState)

# Add nodes
workflow.add_node("generate_cv", generate_cv_node)
workflow.add_node("approval", approval_node)
workflow.add_node("convert_pdf", convert_pdf_node)

# Connect nodes (linear flow)
workflow.set_entry_point("generate_cv")

# Add conditional edge so graph jumps to end if CV generation fails
workflow.add_conditional_edges(
    "generate_cv",
    lambda state: "approval" if state.tailored_cv_path else END,
    {"approval": "approval", END: END}
)

# Conditional edge: only go to convert_pdf if approved, else END
workflow.add_conditional_edges(
    "approval",
    lambda state: "convert_pdf" if state.approved else END,
    {"convert_pdf": "convert_pdf", END: END}
)

# Final step (converting to pdf) always leads to END
workflow.add_edge("convert_pdf", END)

# Add checkpointing (optional, useful for multiple jobs)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# ---- Run example ----
if __name__ == "__main__":
    inputs = {
        "job_listing": "inputs/job_descriptions/job_description.txt",
        "cv_template": "inputs/cv_template/cv_template.docx",
    }
    final_state = app.invoke(inputs, config={"configurable": {"thread_id": "job1"}})

    print("\nFinal state:", final_state)
