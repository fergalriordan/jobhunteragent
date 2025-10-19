# AI Agent Instructions for JobHunterAgent

## Core Architecture

This is a Python-based job application assistant using LangChain for LLM orchestration. Key components:

```
tailored_application_pipeline/
├── cv_pipeline.py       # CV generation engine
├── async_batch.py       # Parallel processing
└── approve_and_finalise.py  # Human approval workflow
```

### Data Flow

1. Input: Job descriptions → `inputs/job_descriptions/`
2. Processing: CV generation via LLM
3. Output: Draft in `outputs/{job_name}/tailored_cv.docx`
4. Approval: Human review → PDF conversion

## Critical Patterns

### Content Generation

```python
# Example from cv_pipeline.py
async def generate_cv(job_desc: str, template: Path) -> dict:
    # 1. Load user profile
    profile = load_user_profile()
    # 2. Generate tailored content via LLM
    content = await llm_client.generate(
        system_prompt=SYSTEM_PROMPT,
        user_profile=profile,
        job_description=job_desc
    )
    # 3. Validate response format
    validate_llm_response(content)
    return content
```

### State Management

- All state changes tracked via file markers (e.g., APPROVED)
- Use `pathlib.Path` for file operations
- Always work with copies, never modify originals

### Error Handling

```python
try:
    await process_job(job_id)
except ContentGenerationError as e:
    logger.error(f"Failed to generate content: {e}", job_id=job_id)
    raise
```

## Integration Points

1. LLM Integration

- Configuration in `tools/prompt/`
- Response format in `tools/prompt/return_format.txt`
- Rate limiting required (max 3 concurrent)

2. Document Processing

- Templates in `.docx` format only
- Use `python-docx` for modifications
- Convert to PDF only after approval

## Development Workflow

1. Running Tests

```bash
pytest tailored_application_pipeline/tests/
```

2. Processing Jobs

```bash
python -m tailored_application_pipeline.async_batch inputs/job_descriptions/
```

3. Approving Results

- Check `outputs/{job_name}/tailored_cv.docx`
- Create APPROVED file
- PDF generates automatically

## Common Pitfalls

1. Template Processing

- Always validate placeholders before processing
- Check compatibility with `validate_template()`

2. Async Operations

- Use `asyncio.gather()` with `return_exceptions=True`
- Clean up resources in `finally` blocks

3. Content Validation

- Always validate LLM responses against schema
- Preserve user's original data truthfulness

## Recommended Reading

1. Key Implementation Files:

- `cv_pipeline.py`: Core generation logic
- `tools/build_prompt.py`: Prompt construction
- `tools/prompt/system_prompt_template.txt`: LLM constraints

2. Configuration:

- Logging: `logs/batch_run.log`
- Templates: `inputs/cv_template/`
- User data: `inputs/user_details/`
