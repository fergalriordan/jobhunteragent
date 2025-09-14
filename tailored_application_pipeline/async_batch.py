import asyncio
import logging
from pathlib import Path
from core import CVPipeline

# ---- Set up logging ----
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/async_batch_run.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def run_job(job_file: Path):
    job_name = job_file.stem
    output_dir = Path(f"outputs/{job_name}")

    try:
        pipeline = CVPipeline(
            job_file=job_file,
            user_details=Path("inputs/user_details/projects.txt"),
            template=Path("inputs/cv_template/cv_template.docx"),
            response_format=Path("inputs/cv_template/response_format.txt"),
        )
        result = pipeline.run(output_dir)

        logging.info(f"{job_name} ✅ Completed. Final state: {result['final_state']}")
        print(f"✅ {job_name} done.")
        return result

    except Exception as e:
        logging.error(f"{job_name} ❌ Failed: {e}", exc_info=True)
        print(f"❌ Error processing {job_name}: {e}")
        return {"job": job_name, "error": str(e)}

async def run_batch():
    job_files = list(Path("inputs/job_descriptions").glob("*.txt"))
    if not job_files:
        print("❌ No job descriptions found.")
        return

    print(f"📄 Found {len(job_files)} job descriptions.")

    # Run jobs concurrently
    results = await asyncio.gather(*(run_job(job) for job in job_files))

    # Write a summary
    logging.info(f"Batch completed. {len(results)} jobs processed.")
    return results

if __name__ == "__main__":
    asyncio.run(run_batch())
