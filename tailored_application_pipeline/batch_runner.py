import os
import glob
import logging
from pathlib import Path
from cv_pipeline import app  # Import your compiled LangGraph workflow

# ---- Setup logging ----
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/batch_run.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_batch():
    # Discover all job description files
    job_files = sorted(glob.glob("inputs/job_descriptions/*.txt"))
    if not job_files:
        print("❌ No job descriptions found in inputs/job_descriptions/")
        return

    print(f"📄 Found {len(job_files)} job descriptions.")

    for idx, job_file in enumerate(job_files, start=1):
        job_name = Path(job_file).stem  # e.g., job1.txt → "job1"
        output_dir = Path(f"outputs/{job_name}")
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n🚀 Processing {job_name} ({idx}/{len(job_files)})")

        # Define tailored CV output paths
        tailored_cv_path = str(output_dir / "tailored_cv.docx")

        inputs = {
            "job_listing": job_file,
            "projects_info": "inputs/user_details/projects.txt",
            "response_format": "inputs/cv_template/response_format.txt",
            "cv_template": "inputs/cv_template/cv_template.docx",
            "tailored_cv_path": tailored_cv_path
        }

        try:
            final_state = app.invoke(inputs, config={"configurable": {"thread_id": job_name}})
            logging.info(f"{job_name} ✅ Completed. Final state: {final_state}")
            print(f"✅ Finished {job_name}.")
        except Exception as e:
            logging.error(f"{job_name} ❌ Failed: {e}")
            print(f"❌ Error processing {job_name}: {e}")

if __name__ == "__main__":
    run_batch()
