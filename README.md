# 🧑‍💼 Job Application Assistant

An experimental **agentic AI system** that automates parts of the job application process.  
Built to explore **LangGraph orchestration**, **document generation pipelines**, and **human-in-the-loop workflows**.

> - ⚠️ This project is intended as a **portfolio/demo** to showcase AI agent design and workflow automation.
> - It also represents exploratory work toward a potential future product.
> - It is **not** intended as a tool for indiscriminate job application spam.  

---

## ✨ Features

- **Tailored CV Generation**  
  - Uses LLMs + template filling to adapt a base CV to each job description.  
  - Customizable prompt templates for flexible style/tone.  

- **Human-in-the-loop Approval**  
  - Drafts require user approval before being finalised.  

- **PDF Conversion & Output Management**  
  - Generates `.docx` drafts and produces polished `.pdf` versions.  
  - Organised per job listing (`outputs/job1/`, `outputs/job2/`, etc.).  

- **Batch Processing**  
  - Supports running on 10-20+ job listings in one session.  
  - Independent state tracking per job using LangGraph checkpointing.  

- **Extensible Pipelines**  
  - Designed to support CVs, cover letters, LinkedIn messages, and more.  
  - Easy to add new document-generation pipelines.  

---

## 🛠️ Tech Stack

- **LangGraph**: State machine orchestration for agent workflows.  
- **LangChain**: LLM-powered document generation.  
- **Python + Pydantic**: Typed state management.  
- **Jinja2**: Prompt templating with variables.  
- **python-docx / reportlab**: Document handling and PDF export.  

---

## 🎯 Roadmap

- Cover Letter pipeline
- LinkedIn message generator
- Web dashboard for approvals
- Spreadsheet integration for tracking applications
- Broader agentic capabilities (company research agents, job/skill trends tracking, etc)

## 📜 License

MIT - free to use and adapt, but please credit this repo if you build on it.