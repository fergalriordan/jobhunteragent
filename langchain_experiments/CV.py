import os
from openai import OpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv


@tool
def tailor_CV():
    """Generate a tailored CV"""
    
    # Load template CV
    with open("cv.txt") as f:
        cv = f.read()

    # Load job description
    with open("job_description.txt") as f:
        job_description = f.read()
    
    # Initialize the client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "developer", "content": "Your job is to tailor the input CV based on the job description. The input CV is quite good already, so you shouldn't make any structural changes - just tweak some of the keywords to better fit with the job description. The changes you make should be subtle - DO NOT GO OVERBOARD."},
            {"role": "user", "content": cv}, 
            {"role": "user", "content": job_description}
        ]
    )
    
    return response.output_text


    