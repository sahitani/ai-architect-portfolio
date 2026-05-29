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