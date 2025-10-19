# JobHunterAssitant Project Context

## Project Overview

JobHunterAssistant is an AI-powered job application assistant that automates and optimizes various aspects of the job application process. The human-in-the-loop system uses LLMs to generate tailored application materials while maintaining truthfulness and professional standards.

### Core Mission
- Automate repetitive aspects of job applications
- Maintain authenticity while optimizing content
- Ensure human oversight of generated content
- Scale application processes efficiently

## Technical Stack

### Core Technologies
- **Language**: Python 3.11+
- **LLM Integration**: LangGraph (built on LangChain)
- **Document Processing**: python-docx
- **PDF Generation**: docx2pdf
- **Async Processing**: Python asyncio
- **State Management**: Pydantic models
- **Logging**: Python logging with structured output

### Project Architecture

```
tailored_application_pipeline/
├── core.py              # Core pipeline orchestration
├── cv_pipeline.py       # CV generation logic
├── async_batch.py       # Batch processing implementation
└── approve_and_finalise.py  # Human-in-loop approval system
```

## Development Guidelines

### Code Style
1. **Type Hints**
   - All function parameters and return types must be typed
   - Use Pydantic models for complex data structures

2. **Error Handling**
   - Custom exceptions for specific error cases
   - Comprehensive error logging
   - Graceful failure handling in async operations

3. **Documentation**
   - Docstrings: Google style
   - Type hints: PEP 484
   - Comments: Only for complex logic explanation

### Project Rules Hierarchy

1. **Data Integrity**
   - Never modify original user data
   - Always work with copies of templates
   - Maintain audit trail of changes

2. **Content Generation**
   - Truth preservation is paramount
   - No fabrication of experience/skills
   - Maintain professional tone
   - Respect user-provided guidelines

3. **Error Handling**
   - Log all errors with context
   - Fail gracefully with user-friendly messages
   - Maintain error state for review

## State Management

### File Organization
```
inputs/
├── cv_template/         # Base templates
├── job_descriptions/    # Target job posts
└── user_details/        # User profile data

outputs/
├── job_description/     # Per-job output
│   ├── APPROVED        # Approval marker
│   ├── final.pdf       # Final approved version
│   └── tailored_cv.docx # Draft version
```

### Process States
1. **Draft**: Initial generated content
2. **Review**: Awaiting human approval
3. **Approved**: Ready for PDF conversion
4. **Final**: PDF generated and ready

## Common Gotchas

1. **Template Processing**
   - Templates must be in .docx format
   - Maintain exact placeholder syntax
   - Check template compatibility before processing

2. **Async Operations**
   - Handle API rate limits
   - Manage memory during batch processing
   - Clean up temporary files

3. **Content Generation**
   - Verify LLM response format
   - Validate against response schema
   - Check for placeholder replacement

## Real-time Context Management

### Session State
- Track current job being processed
- Maintain approval status
- Monitor batch progress

### Environmental Awareness
- Check available API credits
- Monitor system resources
- Track processing time

## Prompt Engineering Guidelines

1. **System Prompts**
   - Maintain consistent persona
   - Include relevant constraints
   - Specify output format

2. **Response Validation**
   - Strict JSON schema compliance
   - Content length limits
   - Professional tone requirements

## Testing Requirements

### Unit Tests
- Mock LLM responses
- Validate document processing
- Check error handling

### Integration Tests
- End-to-end pipeline validation
- Batch processing verification
- PDF conversion accuracy

## Feature Status

### Implemented ✅
- CV generation pipeline
- Batch processing
- Human-in-loop approval
- PDF conversion
- Logging system

### In Progress 🚧
- Cover letter generation
- LinkedIn message creation
- Web UI for approvals

### Planned 📋
- Application Q&A helper
- Company research agent
- Interview preparation assistant

## Performance Considerations

1. **Resource Management**
   - Clean up temporary files
   - Monitor memory usage
   - Handle concurrent operations

2. **API Efficiency**
   - Implement request batching
   - Cache common operations
   - Rate limit API calls

## Security Guidelines

1. **Data Protection**
   - No storage of sensitive data
   - Secure template handling
   - Clean up temporary files

2. **API Security**
   - Secure key management
   - Rate limiting
   - Input validation

---

Note: This context file should be updated as the project evolves. AI assistants should refer to this document for guidance but also apply common sense and best practices where specific guidance is not provided.
