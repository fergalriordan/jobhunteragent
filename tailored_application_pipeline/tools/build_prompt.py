import json

def build_fields_info():
    with open("tools/prompt/fields_info.txt", encoding="utf-8") as f:
        fields_info = f.read()
    
    with open("tools/prompt/user_info/profile_instructions.txt", encoding="utf-8") as f:
        profile_instructions = f.read()
    with open("tools/prompt/user_info/skills.txt", encoding="utf-8") as f:
        skills_info = f.read()
    with open("tools/prompt/user_info/projects.txt", encoding="utf-8") as f:
        projects_info = f.read()
    
    # replace placeholders in fields_info with the relevant text
    fields_info = fields_info.replace("{profile_instructions}", profile_instructions)
    fields_info = fields_info.replace("{skills_info}", skills_info)
    fields_info = fields_info.replace("{projects_info}", projects_info)

    return fields_info

def build_system_prompt():
    with open("tools/prompt/system_prompt_template.txt", encoding="utf-8") as f:
        system_prompt_template = f.read()
    
    with open("tools/prompt/user_info/sample_cv.txt", encoding="utf-8") as f:
        sample_cv = f.read()
    
    with open("tools/prompt/user_info/experience.txt", encoding="utf-8") as f:
        experience_info = f.read()

    fields_info = build_fields_info()

    # replace placeholders in system prompt with the relevant text
    system_prompt_template = system_prompt_template.replace("{sample_cv}", sample_cv)
    system_prompt_template = system_prompt_template.replace("{experience_info}", experience_info)
    system_prompt = system_prompt_template.replace("{fields_info}", fields_info)

    return system_prompt

def build_prompt(job_listing: str):
    system_prompt = build_system_prompt()

    with open("tools/prompt/user_info/example/user.txt", encoding="utf-8") as f:
        example_user_message = f.read()
    
    with open("tools/prompt/user_info/example/assistant.txt", encoding="utf-8") as f:
        example_assistant_message = f.read()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": example_user_message},
        {"role": "assistant", "content": example_assistant_message},
        {"role": "user", "content": f"""
            =====================================================================
            Job Listing:

            {job_listing}

            =====================================================================
            
            Return a tailored CV for this job listing as a JSON object with fields:
            Profile, Technical Skills, Relevant Projects.
            """}
    ]

    with open("tools/prompt/return_format.txt", encoding="utf-8") as f:
        return_format = json.load(f)

    prompt_kwargs = {
        "model": "gpt-4o",
        "input": messages,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "response_format",
                "description": "You must return a valid JSON object where each field represents a CV section. The fields must be tailored based on the job description.",
                "schema": return_format
            }
        },
        "temperature": 0.8
    }

    return prompt_kwargs

if __name__ == "__main__":
    prompt_kwargs = build_prompt()
    print(prompt_kwargs)