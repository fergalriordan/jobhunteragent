from typing import Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from tools.generate_tailored_cv import generate_tailored_cv

load_dotenv()

# ---- Define state ----
class CVPipelineState(BaseModel):
    job_listing: str
    projects_info: str
    cv_template: str
    tailored_cv_path: Optional[str] = None

# ---- Define nodes ----
def generate_cv_node(state: CVPipelineState):
    """Generate tailored CV draft (docx)."""
    try:
        generate_tailored_cv(
            path_to_job_listing=state.job_listing,
            path_to_projects_info=state.projects_info,
            path_to_cv_template=state.cv_template,
            path_to_output_cv=state.tailored_cv_path,
        )
        print(f"✅ Draft CV generated: {state.tailored_cv_path}")
    except Exception as e:
        print(f"❌ Error generating draft CV: {e}")
        state.tailored_cv_path = None
    return state

def failure_node(state: CVPipelineState):
    print("❌ Draft generation failed.")
    return state

# ---- Build LangGraph workflow ----
workflow = StateGraph(state_schema=CVPipelineState)
workflow.add_node("generate_cv", generate_cv_node)
workflow.add_node("failure", failure_node)

workflow.set_entry_point("generate_cv")

workflow.add_conditional_edges(
    "generate_cv",
    lambda state: END if state.tailored_cv_path else "failure",
    {END: END, "failure": "failure"}
)
workflow.add_edge("failure", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
