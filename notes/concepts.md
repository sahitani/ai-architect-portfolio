# Concepts & Mental Models

## Days 1–2: Git, GitHub, Python environment

### Git vs GitHub
- **Git** = software on your laptop managing the hidden `.git` folder
- **GitHub** = a website that hosts copies of `.git` folders
- They're separate. Git existed before GitHub. You can use Git without GitHub.
- "Push" = upload commits to GitHub. Commits exist locally until pushed.

### The three Git states
Working Directory → (git add) → Staging Area → (git commit) → Repository
- **WD:** file on disk as you see it
- **Staging:** "I want this in the next commit"  
- **Repo:** permanent snapshot history

### Why virtual environments
- System Python is shared across projects → one project's package upgrade breaks another
- A `.venv` is an isolated Python installation per project
- Activate it before installing or running anything: `(.venv)` prefix is your visual confirmation
- `.venv` is gitignored (not shared); `requirements.txt` is committed (recreates the env)

### SSH at a glance
- SSH = Secure Shell. Originally for encrypted remote login (replacing insecure Telnet).
- For GitHub: a key pair authenticates you without ever transmitting a password.
- Private key stays on your laptop; public key sits on GitHub.
- One-time setup, then `git push` just works forever.

## Day 3: Python basics

### Dynamic typing
- Variables don't declare a type; Python figures it out at assignment time.
- Convenient for PoCs, dangerous at scale (typos and contract violations only show up at runtime).
- Type hints (`def f(x: int) -> str`) don't enforce at runtime but enable static checking 
  via mypy and IDE warnings.

### F-strings are the foundation of prompt engineering
- `f"text {expression}"` substitutes any Python expression into a string
- Everything outside `{}` is literal text — spaces, hyphens, newlines all matter
- LLMs are sensitive to small formatting differences — be deliberate about whitespace
- Triple-quoted f-strings (`f"""..."""`) preserve line breaks → ideal for multi-paragraph prompts

### Lists, dicts, and the `list[dict]` pattern
- **List `[]`** = ordered, accessed by position. Use for collections where order matters.
- **Dict `{}`** = key-value pairs, accessed by key. Use for named attributes.
- The dominant pattern in AI code is `list[dict]`: chat history, retrieved docs, tool calls, 
  evaluation results. Get fluent at navigating it.
- Chained access (`response["choices"][0]["message"]["content"]`) is one of the most-written 
  patterns in LLM Python code. Trace it left-to-right, one bracket at a time.

### Truthy / falsy
- `if not x:` triggers if `x` is None, 0, empty string, empty list, empty dict, or False
- Pythonic shortcut: `if not retrieved_docs:` checks for empty results without `len() == 0`

## Day 5: Functions

### The core idea
- A function is a named, reusable block of code.
- Two distinct halves: DEFINING (writing the recipe) and CALLING (running it).
- Defining alone does nothing — you must call it to actually run the code.

### Anatomy of a function
    def function_name(parameter1, parameter2):    ← `def`, name, slots, colon
        # body — indented, runs when called
        return value                              ← hands a value back

- `def` opens a block → needs `:` at the end (same rule as `for`, `if`).
- Parameters in `()` are slots; they're filled with values when you call.
- Function name uses `snake_case`.

### Parameters vs arguments
- Parameter = the slot in the definition (e.g. `name` in `def greet(name):`)
- Argument = the actual value passed when calling (e.g. `"Harish"` in `greet("Harish")`)
- People use the words interchangeably in practice. Don't stress.

### Multiple parameters
- Separate with commas: `def f(a, b, c):`
- When calling, pass values in the SAME ORDER as the slots.
- Or name them explicitly: `f(a=1, b=2, c=3)` — more readable, especially for many params.

### print vs return — THE most important distinction
- `print` → shows a value to a HUMAN on screen. Program can't use it afterward. Value is gone.
- `return` → hands a value back to the PROGRAM. Caller can capture it and use it.
- If a function doesn't return anything, Python implicitly returns `None`.
- Telltale bug: `result = some_function(...)` and `result` ends up as `None` → the function
  only printed, didn't return.

### Default parameter values
- Syntax: `def f(prompt, temperature=0.7):` 
- If the caller doesn't supply that argument, the default is used.
- Rule: parameters with defaults must come AFTER parameters without defaults.
- Hugely common in AI libraries: `llm.invoke(prompt, temperature=0.7, max_tokens=1000)`.

### THE BIG CONCEPTUAL INSIGHT: parameter names are private to the function
- The name OUTSIDE a function

## Day 6: Modules, Imports & Error Handling

### Why imports exist
- Python's built-ins are small (~70 things: print, len, range, etc.)
- Real power comes from external code — libraries someone else wrote
- `import` is how you "open a toolbox" and make its tools available

### Built-in vs external modules
- Built-in: math, random, datetime, json — come WITH Python, just `import` them
- External: requests, rich, langchain, openai — must be `pip install`-ed first, THEN imported

### Two import styles
    import math               → use as `math.sqrt(16)`
    from math import sqrt     → use as `sqrt(16)` directly
- The first preserves the module name (clearer about where things come from)
- The second is concise (preferred when you only need 1-2 things from a library)
- AI code overwhelmingly uses the second style

### Renaming on import
    import numpy as np        # convention across the data science world
    import pandas as pd       # same
    from rich import print as rich_print   # avoid conflict with built-in print
- `as <new_name>` renames the import locally

### The dot-navigation pattern
- `module.thing` reaches into a module to get a specific tool
- Multiple dots = navigating nested compartments:
    datetime.datetime.now()
    openai.chat.completions.create(...)
- Same as folder paths — outside in.

### The install-import-use lifecycle (per new library)
1. `pip install <name>`        # once per project (PowerShell prompt)
2. `import <name>`             # in every script that uses it
3. `<name>.something(...)`     # actually use it

### Error handling with try/except
- Without it: any error CRASHES the program
- With it: errors are caught and you decide what to do
- Shape:
      try:
          risky_operation()
      except SomeErrorType:
          handle_it()
- Catch a specific error type when you know what can go wrong
- `except Exception as e` catches anything; `e` holds the actual error message
- Both `try:` and `except:` open blocks → both need `:` at the end

### The AI production pattern (loop + try/except)
    for item in many_items:
        try:
            result = risky_thing(item)
            save(result)
        except APIError:
            log_and_skip(item)
            continue
- This is the difference between PoC code (crashes on first failure) and 
  production code (processes millions of items reliably)

### TWO BIG TERMINAL LESSONS

#### Lesson 1: Two prompts, two languages
- PowerShell prompt `(.venv) PS C:\...>` → for terminal commands (pip, git, python, cd)
- Python interactive prompt `>>>` → for Python code (print, import, function calls)
- Typing Python at PowerShell → "not recognized as a cmdlet..."
- Typing PowerShell at Python → "SyntaxError: invalid syntax"
- The error message tells you which prompt you're at by which language it speaks

#### Lesson 2: Fresh session vs persistent session
- `python filename.py` → starts FRESH session, runs file top-to-bottom, dies. 
  No memory between runs. Same input → same output. Predictable.
- `python` (alone) → starts an interactive `>>>` session that PERSISTS until you exit().
  Things you define stay in memory. Convenient but can cause "leftover state" confusion.
- Mystery output? First suspect: leftover state from a persistent session. 
  Fix: restart the session.

### Workflow recommendation (current phase)
- Default: write code in `.py` files, run with `python filename.py`
- The file is your permanent record. Each run is fresh and predictable.
- Use interactive `>>>` only for quick throwaway experiments.
- We'll switch to Jupyter notebooks later when AI experimentation needs persistent state.

## Day 7: Putting It All Together — The Document Analyzer

### What the analyzer demonstrates structurally
A small but real Python tool combining everything from Days 3-6:
- Multiple functions, one calling another (composition)
- Loop over a list of items
- Each item processed by calling functions, results stored as dicts
- Final output: list of dicts (the AI workhorse pattern)
- Error handling with try/except + separate failure tracking
- External library (rich) used for professional output

### The architectural pattern: "collect then report"
Real engineering habit worth internalizing:
    Loop 1: compute all the data, store in a list of dicts
    Loop 2: display the data (or send it elsewhere)
Benefits:
- The data becomes reusable (sort, filter, save, pass elsewhere)
- What you compute is separated from how you show it
- Swapping the report format doesn't touch the analysis logic
- Scales naturally when error handling enters the picture

### Production error handling pattern
    results = []
    failures = []
    for item in items:
        try:
            results.append(process(item))
        except Exception as e:
            failures.append({"item": item, "error": str(e)})
- Two separate lists — never lump successes and failures together
- str(e) converts the exception object to a string for storage
- `if failures:` uses truthy/falsy to conditionally report only when needed
- This is the difference between a script that "crashes on bad input" and 
  one that "processes a batch reliably"

### Functions calling functions (composition)
    def count_words(text): return len(text.split())
    def estimate_cost(text): return count_words(text) * 1.3 * price
- `estimate_cost` USES `count_words` internally
- One source of truth — if word counting logic changes, both stay aligned
- This is how complex pipelines are built: small functions composing into 
  larger workflows

### Small Python details picked up today
- **String slicing:** `doc[:50]` — first 50 characters (same shape as list slicing)
- **String concatenation:** `"hello" + " " + "world"` joins strings with `+`
- **Type conversion:** `str(123)` → `"123"`, `int("5")` → `5`
- **Newline character:** `\n` inside a string = "go to a new line here"
- **Quote nesting in f-strings:** if outside uses `"`, use `'` inside the {}
  (or vice versa) — avoids confusion about where the string ends

### What this tool is structurally similar to
The skeleton of a RAG ingestion pipeline:
    for doc in documents:
        try:
            chunks = chunk_document(doc)
            embeddings = embed(chunks)
            save_to_vector_db(embeddings)
        except Exception as e:
            log_failure(doc, e)
Same shape. Today's body is simpler (count words, estimate cost).
Phase 1 will swap the body for real AI operations.