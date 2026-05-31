def word_count(text):
    word_number = len(text.split())
    return word_number

my_text = "Hello world from Harish"
total = word_count(my_text)
print(f"Total number of words: {total}")


import math

print(math.sqrt(16))
print(math.pi)

import datetime
 
now = datetime.datetime.now()
print(now)

today = datetime.date.today()
print(today)

from math import sqrt

print(sqrt(16))         # use it directly, no math. prefix needed

# Way 1: import the whole module
import random
print(random.choice(["A", "B", "C"]))

# Way 2: import just what you need
from random import choice
print(choice(["A", "B", "C"]))

from rich import print as rich_print
from rich.table import Table

# Colored, styled output
rich_print("[bold green]Day 6 — using my first external library![/bold green]")
rich_print("[italic blue]This text is in italic blue.[/italic blue]")

# A nicely formatted table
table = Table(title="LLM Models")
table.add_column("Name", style="cyan")
table.add_column("Provider", style="magenta")
table.add_column("Context Window", style="yellow")

table.add_row("gpt-4", "OpenAI", "8K tokens")
table.add_row("claude-3-opus", "Anthropic", "200K tokens")
table.add_row("llama-3", "Meta", "8K tokens")

rich_print(table)

try:
    bad = int("hello")    # can't convert "hello" to a number
except Exception as e:
    print(f"Something went wrong: {e}")