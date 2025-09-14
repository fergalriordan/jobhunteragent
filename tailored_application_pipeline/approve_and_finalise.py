import logging
from pathlib import Path
from tools.convert_to_pdf import convert_to_pdf

# ---- Set up logging ----
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/approval_run.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def process_approvals():
    output_root = Path("outputs")
    for job_dir in output_root.iterdir():
        if not job_dir.is_dir():
            continue

        draft = job_dir / "tailored_cv.docx"
        pdf = job_dir / "final.pdf"
        approved = job_dir / "APPROVED"
        rejected = job_dir / "REJECTED"

        if approved.exists() and draft.exists() and not pdf.exists():
            try:
                convert_to_pdf(draft, pdf)
                logging.info(f"{job_dir.name} ✅ Approved and converted to {pdf}")
                print(f"✅ {job_dir.name} finalized.")
            except Exception as e:
                logging.error(f"{job_dir.name} ❌ Failed to finalize: {e}", exc_info=True)
                print(f"❌ Error finalizing {job_dir.name}: {e}")

        elif rejected.exists():
            logging.info(f"{job_dir.name} ❌ Rejected by user.")
            print(f"🚫 {job_dir.name} rejected, skipping.")
        else:
            print(f"⏳ {job_dir.name} waiting for approval...")

if __name__ == "__main__":
    process_approvals()
