from rich.console import Console
from rich.table import Table

def count_words(text):
    return len(text.split())

def estimate_cost(text, price_per_token=0.00003):
    estimated_tokens = count_words(text) * 1.3
    return estimated_tokens * price_per_token

console = Console()

documents = [
    "Python is a high-level programming language used widely in data science and AI.",
    "Retrieval-Augmented Generation combines vector search with language model generation.",
    None,
    "LangChain is a framework that simplifies building applications powered by language models."
]

# Process each document
results = []
failures = []

for doc in documents:
    try:
        analysis = {
            "document": doc,
            "word_count": count_words(doc),
            "estimated_cost": estimate_cost(doc)
        }
        results.append(analysis)
    except Exception as e:
        failures.append({"document": doc, "error": str(e)})

# Display results
table = Table(title="Document Analysis Results")
table.add_column("Document Preview", style="cyan", overflow="fold")
table.add_column("Word Count", style="yellow", justify="right")
table.add_column("Estimated Cost", style="green", justify="right")

for item in results:
    preview = item["document"][:60] + "..."
    table.add_row(
        preview,
        str(item["word_count"]),
        f"${item['estimated_cost']:.6f}"
    )

console.print(table)

if failures:
    console.print(f"\n[bold red]{len(failures)} document(s) failed:[/bold red]")
    for f in failures:
        console.print(f"  [red]•[/red] {f['document']} → [italic]{f['error']}[/italic]")