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