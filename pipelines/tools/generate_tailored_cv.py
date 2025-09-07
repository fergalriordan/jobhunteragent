import json
from openai import OpenAI
from docxtpl import DocxTemplate, RichText

def load_static_cv_data(cv_data: dict, projects_info_file_path: str):
    """
    Load static data associated with dynamically selected CV components
    For example, the LLM chooses which projects to include, but the dates associated with these projects are static
    The static components are inserted independently to reduce errors
    """
    with open(projects_info_file_path, "r", encoding="utf-8") as f:
        projects = json.load(f)

    for i, project in enumerate(cv_data["Relevant Projects"]):
        project_title = project["Title"]
        if project_title in projects:
            details = projects[project_title]
            cv_data["Relevant Projects"][i]["Dates"] = details.get("Dates", "")
            cv_data["Relevant Projects"][i]["Link"] = details.get("Link", "")
            cv_data["Relevant Projects"][i]["Description"] = details.get("Description", "")

def render_cv_to_docx(cv_data: dict, projects_info_file_path: str, template_file_path: str, output_file_path: str):
    """
    Insert LLM-generated tailored CV components into template CV
    Returns:
        str: Path to the output CV
    """
    load_static_cv_data(cv_data, projects_info_file_path)

    # Preprocess template to preserve ampersands in static text
    doc = DocxTemplate(template_file_path)

    # Build RichText hyperlinks for the two projects
    project_1_link = RichText()
    link_1 = cv_data["Relevant Projects"][0].get("Link", "")
    if link_1:
        project_1_link.add("View Project", url_id=doc.build_url_id(link_1))

    project_2_link = RichText()
    link_2 = cv_data["Relevant Projects"][1].get("Link", "")
    if link_2:
        project_2_link.add("View Project", url_id=doc.build_url_id(link_2))

    # Rename keys for Jinja (no spaces, consistent with template placeholders)
    context = {
        "Profile": cv_data["Profile"],
        "Key_Competencies": cv_data["Technical Skills"]["Key Competencies"],
        "Programming_Languages": cv_data["Technical Skills"]["Programming Languages"],
        "Frameworks_and_Libraries": cv_data["Technical Skills"]["Frameworks & Libraries"],
        "Tools_and_Platforms": cv_data["Technical Skills"]["Tools & Platforms"],
        "Project_1_Title": cv_data["Relevant Projects"][0]["Title"],
        "Project_1_Dates": cv_data["Relevant Projects"][0]["Dates"],
        "Project_1_Skills": cv_data["Relevant Projects"][0]["Skills"],
        "Project_1_Link": project_1_link,
        "Project_1_Description": cv_data["Relevant Projects"][0]["Description"],
        "Project_2_Title": cv_data["Relevant Projects"][1]["Title"],
        "Project_2_Dates": cv_data["Relevant Projects"][1]["Dates"],
        "Project_2_Skills": cv_data["Relevant Projects"][1]["Skills"],
        "Project_2_Link": project_2_link,
        "Project_2_Description": cv_data["Relevant Projects"][1]["Description"],
    }

    print("Starting attempt")
    doc.render(context)
    doc.save(output_file_path)
    print("Attempt complete")
    print(f"CV saved to {output_file_path}")

def generate_tailored_cv(path_to_job_listing: str, path_to_projects_info: str, path_to_response_format: str, path_to_cv_template: str, path_to_output_cv: str) -> str:
    """
    Generate a tailored CV for job listing.
    The CV is stored in a word document which the user can inspect and edit.
    If they deem it to be acceptable, they can request for it to be converted to a pdf.
    """
    try:
        client = OpenAI()

        with open(path_to_job_listing, "r", encoding="utf-8") as f:
            job_listing = f.read()

        with open(path_to_response_format, "r", encoding="utf-8") as f:
            response_format = json.load(f)

        response = client.responses.create(
            input=f"""
            =====================================================================
            Job Listing:

            {job_listing}
            =====================================================================
            
            Return a tailored CV for this job listing as a JSON object with fields:
            Profile, Technical Skills, Relevant Projects.
            """,
            prompt={
                "id": "pmpt_68b0c358291c81968a00e9414e386276009a458f13092457",
                "version": "13"
            },
            text=response_format  # schema for structured model output
        )

        cv_data = json.loads(response.output_text)
        print(json.dumps(cv_data, indent=2))
        render_cv_to_docx(cv_data, path_to_projects_info, path_to_cv_template, path_to_output_cv)

    except Exception as e:
        print(f"Error generating CV: {e}")
        raise
