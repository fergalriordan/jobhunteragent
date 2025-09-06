import json
from langchain_core.tools import tool
from openai import OpenAI
from docxtpl import DocxTemplate, RichText

def load_static_cv_data(cv_data):
    with open("projects.txt", "r", encoding="utf-8") as f:
        projects = json.load(f)

    for i, project in enumerate(cv_data["Relevant Projects"]):
        project_title = project["Title"]
        if project_title in projects:
            details = projects[project_title]
            cv_data["Relevant Projects"][i]["Dates"] = details.get("Dates", "")
            cv_data["Relevant Projects"][i]["Link"] = details.get("Link", "")
            cv_data["Relevant Projects"][i]["Description"] = details.get("Description", "")

def render_cv_to_docx(cv_data: dict, template_file="cv_template.docx", output_file="tailored_cv.docx"):
    
    load_static_cv_data(cv_data) # Add static cv data based on the projects etc selected by the model

    doc = DocxTemplate(template_file)

    # Build RichText hyperlinks for the two projects
    project_1_link = RichText()
    project_1_link.add("View Project", url_id=doc.build_url_id(cv_data["Relevant Projects"][0]["Link"]))

    project_2_link = RichText()
    project_2_link.add("View Project", url_id=doc.build_url_id(cv_data["Relevant Projects"][1]["Link"]))

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
    doc.save(output_file)
    print("Attempt complete")
    print(f"CV saved to {output_file}")
    return output_file

@tool
def generate_tailored_cv(path_to_job_listing: str) -> str: 
    """
    Generate a tailored CV for job listing.
    The CV is stored in a word document which the user can inspect and edit.
    If they deem it to be acceptable, they can request for it to be converted to a pdf.
    Returns:
        str: Path to the tailored CV document, or an empty string if an error was encountered.
    """

    try:
        client = OpenAI()

        with open(path_to_job_listing) as f:
            job_listing = f.read()
        
        with open("response_format.txt", "r", encoding="utf-8") as f:
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
            text=response_format # schema for structured model output
        )

        cv_data = json.loads(response.output_text)
        print(json.dumps(cv_data, indent=2))
        output_file_path = render_cv_to_docx(cv_data=cv_data)

        return output_file_path
    
    except:
        return ""