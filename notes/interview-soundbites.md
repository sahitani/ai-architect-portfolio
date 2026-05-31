# AI Architect Interview Soundbites

## Python's dynamic typing
- **PoC:** No type declarations, write fast
- **Enterprise:** Type hints + mypy in CI catches contract violations pre-prod
- **Soundbite:** "The cost of writing `tokens: int` once is repaid every 
  time someone refactors the function six months later."

## Prompt construction
- **PoC:** Inline f-string prompts in the function that uses them
- **Enterprise:** Externalized prompt templates (LangChain PromptTemplate, prompt registries 
  like LangSmith/Humanloop), versioned, testable, editable by non-engineers
- **Soundbite:** "Treating prompts as code — versioned, externalized, tested — is a 
  major maturity marker for AI engineering teams."

## Configuration handling
- **PoC:** Plain dicts inline in scripts
- **Enterprise:** Typed config objects (Pydantic models), bounded validation, environment-based 
  loading from `.env`, secrets externalized
- **Soundbite:** "The hour spent defining the schema saves a week of 'why is the temperature 
  suddenly 7.0' incidents."

  ## Functions as the AI pipeline skeleton
- AI pipelines are functions handing values to each other via `return`:
  chunks = split_document(doc)
  embeddings = embed(chunks)
  results = search(query, embeddings)
  answer = generate(query, results)
- **Soundbite:** "Every AI system I've built is fundamentally a composition of small functions —
  each does one thing, returns a clean output, and chains into the next. That separation
  is what makes the pipeline testable, observable, and replaceable component-by-component."

  ## Error handling philosophy (PoC vs Enterprise)
- **PoC:** Optimistic code, no error handling — crashes on first failure
- **Enterprise:** Per-item try/except, structured logging, retry with exponential backoff
  (via `tenacity`), separate tracking of successes and failures, checkpointing for resume
- **Soundbite:** "LLM APIs are inherently flaky. Designing for resilience from the start — 
  per-call retries, batch-level error isolation, and structured failure logging — prevents 
  the painful retrofit from a hackathon prototype to a production pipeline. The shape is 
  always: loop + try/except + continue, not loop + crash."

## Dependency management
- **PoC:** `pip install X` and move on
- **Enterprise:** Pinned versions in `requirements.txt` (or `pyproject.toml` + Poetry/uv), 
  isolated venvs per project, reproducible builds via lock files, security scanning of 
  dependencies (e.g., `pip-audit`, Dependabot)
- **Soundbite:** "Reproducible environments are foundational. A pinned requirements file 
  means a teammate, a CI runner, and the production container all get the exact same 
  package versions — which is the difference between 'works on my machine' and 
  'works everywhere.'"

  ## Separation of concerns: compute vs display
- **PoC:** Print results inline as you compute them
- **Enterprise:** Compute first into structured data (list of dicts, dataframes, 
  Pydantic models); display/serialize as a separate concern
- **Soundbite:** "I separate computation from presentation from the start. The analysis 
  function returns structured data; another layer renders it as JSON, a table, or a 
  dashboard. This means we can swap the output format without changing the logic — 
  whether it's a CLI report today or a Streamlit dashboard next month."

## Error isolation in batch processing
- **PoC:** Loop processes items optimistically; one failure kills everything
- **Enterprise:** Per-item try/except, separate success/failure collections, structured
  failure logs, observable success rates over time
- **Soundbite:** "One malformed document should never kill the processing of 9,999 good 
  ones. I always design batch pipelines with per-item error isolation and separate 
  tracking of failures. It costs almost nothing in code complexity but is the difference 
  between a hackathon script and a system you can run unattended."

## Function composition for pipeline design
- Small functions that each do one thing, composed into larger workflows
- Each function returns clean structured output that becomes input to the next
- **Soundbite:** "AI pipelines are fundamentally function composition — chunk, embed, 
  store, retrieve, generate. Each step is a function with a clear contract. That 
  separation is what makes the pipeline testable component-by-component, observable at 
  each stage, and replaceable when a better embedding model or vector store comes out."