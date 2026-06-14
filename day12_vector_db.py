import chromadb
from chromadb.utils import embedding_functions

# Define a custom embedding function using sentence-transformers
# This is how ChromaDB knows to use a specific model for embeddings
custom_embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

#CHANGE 1: Use PersistentClient instead of Client, with a directory path
client = chromadb.PersistentClient(path="./chroma_db")

# CHANGE 2: Use get_or_create_collection — won't fail if it already exists
collection = client.get_or_create_collection(
    name="company_docs",
    embedding_function=custom_embedding_fn,
    metadata={"hnsw:space": "cosine"}
)

# Only add documents if the collection is empty (avoid duplicate inserts on re-runs)
if collection.count() == 0:
    collection.add(
        documents=[
            "Our return policy allows 30 days for unopened items.",
            "The login API endpoint accepts POST requests with email and password.",
            "We offer flexible work hours and remote work options.",
            "To deploy a service, use the kubectl apply command in our cluster.",
            "Annual leave entitlement is 24 days for full-time employees.",
        ],
        ids=["doc1", "doc2", "doc3", "doc4", "doc5"],
        metadatas=[
            {"department": "sales", "doc_type": "policy"},
            {"department": "engineering", "doc_type": "technical"},
            {"department": "hr", "doc_type": "policy"},
            {"department": "engineering", "doc_type": "technical"},
            {"department": "hr", "doc_type": "policy"},
        ]
    )
    print(f"Ingested {collection.count()} documents into the persistent database.")
else:
    print(f"Collection already contains {collection.count()} documents (persisted from previous run).")

print()

# Same Query 1 as before — let's compare distances
print("=== Query: 'How do I make a service live?' (no filter, cosine distance) ===")
results = collection.query(
    query_texts=["How do I make a service live?"],
    n_results=3
)
for i, doc in enumerate(results["documents"][0]):
    meta = results["metadatas"][0][i]
    distance = results["distances"][0][i]
    similarity = 1 - distance  # convert cosine distance to similarity
    print(f"  [{meta['department']}] (dist: {distance:.3f}, sim: {similarity:.3f}) {doc}")