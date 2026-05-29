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