# Cheatsheet

## Daily workflow
cd C:\dev\ai-architect-portfolio
.venv\Scripts\Activate.ps1          # look for (.venv) in prompt
code .                              # open in VS Code
... work ...
git add .
git commit -m "meaningful message"
git push

## Git commands
| Command | What it does |
|---|---|
| `git status` | Show staged, unstaged, untracked |
| `git add <file>` | Stage one file |
| `git add .` | Stage all changes |
| `git commit -m "..."` | Commit staged changes |
| `git push` | Upload commits to GitHub |
| `git log --oneline` | Compact history |
| `git remote -v` | Show remotes |

## Python data types
| Type | Example | Notes |
|---|---|---|
| `str` | `"text"` | Use double quotes; `"""..."""` for multi-line |
| `int` | `42` | Whole numbers |
| `float` | `0.7` | Decimals |
| `bool` | `True`, `False` | Capitalized |
| `None` | `None` | "no value" |

## F-strings
```python
name = "Harish"
f"Hello, {name}!"                          # basic
f"Cost: ${tokens * price:.4f}"             # expression + format
f"""multi-line
prompt with {variable}"""                  # triple quotes
```

## List operations
```python
items = ["a", "b", "c"]
items[0]            # first item
items[-1]           # last item
items[1:3]          # slice
items.append("d")   # add to end
len(items)          # length
"a" in items        # membership check
```

## Dict operations
```python
config = {"key": "value"}
config["key"]                  # access (crashes if missing)
config.get("key", default)     # safe access with default
config["new"] = "v"            # add or update
"key" in config                # membership check
for k, v in config.items():    # iterate key-value
```

## Control flow
```python
# if/elif/else
if x < 5:
    ...
elif x < 10:
    ...
else:
    ...

# for loop
for item in items:
    ...

# for with index
for i, item in enumerate(items):
    ...

# range
range(5)           # 0,1,2,3,4
range(1, 6)        # 1,2,3,4,5
range(0, 100, 10)  # 0,10,20,...,90

# list comprehension
filtered = [x for x in items if condition(x)]
```

## Common comparisons & logic
| Operator | Meaning |
|---|---|
| `==` `!=` | Equal / not equal |
| `<` `>` `<=` `>=` | Comparisons |
| `in` `not in` | Membership |
| `and` `or` `not` | Logical |

## Functions

### Define
    def greet(name):                       # one parameter
        print(f"Hello, {name}!")

    def add(a, b):                         # multiple parameters
        return a + b

    def call_llm(prompt, temperature=0.7): # default value
        ...

### Call
    greet("Harish")                        # positional
    add(3, 5)                              # → 8 (returned)
    call_llm("Hi")                         # uses default temperature
    call_llm("Hi", temperature=1.2)        # overrides default

### Capture a returned value
    result = add(3, 5)        # result holds 8
    print(result)

### return vs print
    def square_print(x):
        print(x * x)          # shows on screen; returns None implicitly

    def square_return(x):
        return x * x          # hands value back

    a = square_print(4)       # prints 16, then a = None
    b = square_return(4)      # prints nothing, b = 16

### Useful string method seen today
    "hello world".split()     # → ["hello", "world"] (split on whitespace)
    len("hello world".split()) # → 2 (word count)

    ## Imports
```python
# Whole module
import math
math.sqrt(16)              # → 4.0

# Specific thing from module
from math import sqrt
sqrt(16)                   # → 4.0

# Multiple things
from math import sqrt, pi

# Rename on import (very common in AI/data world)
import numpy as np
import pandas as pd
from rich import print as rich_print
```

## Install a new library

## The `list[dict]` build pattern (with append)
```python
results = []
for item in items:
    record = {
        "field1": some_function(item),
        "field2": another_function(item),
    }
    results.append(record)
# results is now a list of dicts, ready to use
```

## Production try/except pattern
```python
results = []
failures = []

for item in items:
    try:
        results.append(process(item))
    except Exception as e:
        failures.append({"item": item, "error": str(e)})

# Report
if failures:
    print(f"{len(failures)} failed")
```

## Rich library basics
```python
from rich.console import Console
from rich.table import Table

console = Console()

# Styled text
console.print("[bold green]Success![/bold green]")
console.print("[red]Error[/red] occurred")

# Tables
table = Table(title="Results")
table.add_column("Name", style="cyan")
table.add_column("Value", style="yellow", justify="right")
table.add_row("First", "100")
console.print(table)
```

## String operations seen today
```python
text[:50]               # first 50 characters (slice)
"a" + "b"               # concatenate → "ab"
str(123)                # int to string → "123"
"line1\nline2"          # \n = newline
```

## The interactive vs file-run distinction (from Day 6)
| Goal | Command |
|---|---|
| Run a whole file fresh | `python filename.py` at PowerShell |
| Open interactive Python session | `python` alone at PowerShell |
| Exit interactive session | `exit()` at `>>>` |

## Groq API call (the standard shape)
```python
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are an AI engineering expert."},
        {"role": "user", "content": "What is RAG?"}
    ]
)
reply = response.choices[0].message.content
```

## .env loading pattern
```python
import os
from dotenv import load_dotenv

load_dotenv()                                # reads .env file
api_key = os.getenv("GROQ_API_KEY")          # gets the value (None if missing)
```

## The Python file template (use for EVERY new file)
```python
# 1. Imports
import os
from somewhere import something

# 2. Module-level setup (runs once on import)
load_dotenv()
client = SomeClient(...)

# 3. Function/class definitions
def my_function(x):
    """One-line description."""
    return x * 2

# 4. Direct-run-only code (skipped on import)
if __name__ == "__main__":
    result = my_function(5)
    print(result)
```

## Groq models to know (current)
| Model | Use case |
|---|---|
| `llama-3.1-8b-instant` | Fast, cheap, decent quality |
| `llama-3.3-70b-versatile` | Higher quality, still fast on Groq |
| `mixtral-8x7b-32768` | Long context (32K tokens) |

## Three message roles
| Role | Purpose |
|---|---|
| `system` | Background instructions / persona / constraints |
| `user` | The human's message |
| `assistant` | The LLM's previous reply (for multi-turn conversations) |

## Quick safety check before EVERY commit

## The four levers of prompt engineering
1. System message (who/rules)
2. User message (task)
3. Examples (few-shot)
4. Parameters (temperature, etc.)

## Structured JSON prompt template
```python
system_msg = """You are a [role].

Return a JSON object with EXACTLY these keys:
- "field1": [allowed values]
- "field2": [allowed values]

Rules:
- Respond with ONLY the JSON object
- No markdown fences, no preamble
- All keys must be present
- Use lowercase for string values"""
```

## JSON parsing
```python
import json

# Native parsing (crashes on malformed JSON)
parsed = json.loads(raw_response)

# Defensive parsing (handles markdown fences)
def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    return json.loads(text)
```

## Pattern: classification with defensive failure
```python
def classify_X(input_text):
    try:
        raw = ask_llm(prompt=input_text, system_message=schema_prompt)
        return extract_json(raw)
    except json.JSONDecodeError:
        return None    # caller decides what to do on failure
```

## JSON ↔ Python type mapping
| JSON | Python |
|---|---|
| "text" | str |
| 42 | int |
| 3.14 | float |
| true / false | True / False |
| null | None |
| [1, 2] | list |
| {"k": "v"} | dict |

## Loading a file
```python
with open("data/file.txt", "r", encoding="utf-8") as f:
    text = f.read()
```

## Chunking patterns (escalating sophistication)
```python
# Strategy 1: Fixed character chunks (PoC)
for start in range(0, len(text), chunk_size):
    chunks.append(text[start:start + chunk_size])

# Strategy 2: With overlap
step = chunk_size - overlap
for start in range(0, len(text), step):
    chunks.append(text[start:start + chunk_size])

# Strategy 3: Boundary-aware — production approach is to use a library:
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_text(text)
```

## The decision tree for chunk_size and overlap
| Document type | chunk_size | overlap |
|---|---|---|
| Narrative text (books, articles) | 500-1500 | 100-200 |
| Code | 1000-2000 | 100 (boundary-aware on functions) |
| Q&A or short docs | 200-500 | 50 |
| Technical documentation | 800-1200 | 100-150 |

Rule of thumb: chunk_size ≈ a few paragraphs; overlap ≈ 1-2 sentences.

## Path conventions
- Always use forward slashes (`/`) in Python paths — works on Windows too
- Use relative paths (`data/file.txt`) for portability
- For complex paths, use `pathlib.Path` (covered later)

## Sentence-Transformers (embeddings)
```python
from sentence_transformers import SentenceTransformer

# Load once at module level (expensive)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed one text
embedding = model.encode("hello")    # → 384-dim numpy array

# Embed many (much faster per item)
embeddings = model.encode(["a", "b", "c"])    # → shape (3, 384)
```

## Cosine similarity (the standard for semantic search)
```python
import numpy as np

def cosine_similarity(vec1, vec2):
    dot = np.dot(vec1, vec2)
    return dot / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
```

## Embedding model dimensions to know
| Model | Dimensions | Notes |
|---|---|---|
| all-MiniLM-L6-v2 | 384 | Fast, free, good for English |
| all-mpnet-base-v2 | 768 | Higher quality, slower |
| OpenAI text-embedding-3-small | 1536 | Hosted, paid, very good |
| OpenAI text-embedding-3-large | 3072 | Hosted, paid, best |

## Cosine similarity interpretation (rough)
| Score | Meaning |
|---|---|
| > 0.7 | Very similar (paraphrases, same topic) |
| 0.4-0.7 | Related |
| 0.2-0.4 | Weakly related |
| < 0.2 | Essentially unrelated |

## The standard RAG retrieval pattern
```python
# At query time:
query_embedding = embed_text(user_question)
similarities = [cosine_similarity(query_embedding, chunk_emb) 
                for chunk_emb in stored_embeddings]
# Get top N indices by similarity
top_n_indices = sorted(range(len(similarities)), 
                       key=lambda i: similarities[i], 
                       reverse=True)[:5]
top_chunks = [stored_chunks[i] for i in top_n_indices]
```
This is conceptually what a vector database does internally — but with ANN indexes that make it fast at scale.

## NumPy array vs Python list
- NumPy arrays look similar but are optimized for math
- `arr.shape` gives dimensions; `(384,)` means 384-element vector
- Most operations are 100x faster than Python list equivalents
- You can slice them like lists: `arr[:10]`

## ChromaDB — the patterns to remember

### Setup with custom embedding & cosine distance & persistence
```python
import chromadb
from chromadb.utils import embedding_functions

custom_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="my_collection",
    embedding_function=custom_fn,
    metadata={"hnsw:space": "cosine"}  # cosine instead of L2
)
```

### Adding documents (with metadata)
```python
collection.add(
    documents=["text1", "text2"],
    ids=["doc1", "doc2"],
    metadatas=[
        {"source": "file_a.pdf", "department": "eng"},
        {"source": "file_b.pdf", "department": "hr"}
    ]
)
```

### Querying — pure semantic
```python
results = collection.query(
    query_texts=["my question"],
    n_results=5
)
# Access:
results["documents"][0]   # list of top matches (first query's results)
results["distances"][0]   # corresponding distances
results["metadatas"][0]   # corresponding metadata dicts
results["ids"][0]         # corresponding IDs
```

### Querying — with metadata filter
```python
# Single condition
results = collection.query(
    query_texts=["my question"],
    n_results=5,
    where={"department": "engineering"}
)

# Compound conditions
results = collection.query(
    query_texts=["my question"],
    n_results=5,
    where={"$and": [
        {"department": "engineering"},
        {"doc_type": "technical"}
    ]}
)
```

### Filter operators
| Operator | Meaning |
|---|---|
| `{"key": "value"}` | equals |
| `{"key": {"$ne": "value"}}` | not equals |
| `{"key": {"$gt": 5}}` | greater than |
| `{"key": {"$in": ["a", "b"]}}` | value in list |
| `{"$and": [...]}` | all conditions must match |
| `{"$or": [...]}` | any condition matches |

### Empty-collection guard (avoid duplicate inserts on re-runs)
```python
if collection.count() == 0:
    collection.add(...)
```

### Production .gitignore additions for vector DB work