from pathlib import Path
from cv_pipeline import app

class CVPipeline:
    def __init__(self, job_file: Path, user_details: Path, template: Path, response_format: Path):
        self.job_file = job_file
        self.user_details = user_details
        self.template = template
        self.response_format = response_format

    def run(self, output_dir: Path) -> dict:
        output_dir.mkdir(parents=True, exist_ok=True)
        tailored_cv_path = output_dir / "tailored_cv.docx"

        inputs = {
            "job_listing": str(self.job_file),
            "projects_info": str(self.user_details),
            "response_format": str(self.response_format),
            "cv_template": str(self.template),
            "tailored_cv_path": str(tailored_cv_path),
        }

        final_state = app.invoke(inputs, config={"configurable": {"thread_id": self.job_file.stem}})
        return {
            "job": self.job_file.stem,
            "final_state": final_state,
            "tailored_cv": tailored_cv_path,
        }
