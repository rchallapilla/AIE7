import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders.csv_loader import CSVLoader
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import SimpleEvolution, NodeFilter
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load your data
loader = CSVLoader(
    file_path="./data/complaints.csv",
    metadata_columns=[
        "Date received", 
        "Product", 
        "Sub-product", 
        "Issue", 
        "Sub-issue", 
        "Consumer complaint narrative", 
        "Company public response", 
        "Company", 
        "State", 
        "ZIP code", 
        "Tags", 
        "Consumer consent provided?", 
        "Submitted via", 
        "Date sent to company", 
        "Company response to consumer", 
        "Timely response?", 
        "Consumer disputed?", 
        "Complaint ID"
    ]
)

documents = loader.load()

# Create embeddings and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(documents[:50])  # Use first 50 docs for demo

vectorstore = Qdrant.from_documents(
    split_docs,
    embeddings,
    location=":memory:",
    collection_name="loan_complaints"
)

# Create knowledge graph from the vector store
from ragas.testset.knowledge_graph import KnowledgeGraph

# Create knowledge graph with proper node creation
kg = KnowledgeGraph.from_langchain_documents(
    documents=split_docs,
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1),
    embeddings=embeddings,
    chunk_size=1000,
    chunk_overlap=200
)

# Create a custom filter that accepts all nodes (or modify as needed)
def custom_filter(node):
    """Custom filter that accepts all nodes with a summary"""
    return node.properties.get("summary") is not None and len(node.properties.get("summary", "")) > 10

# Create the testset generator with proper configuration
generator = TestsetGenerator.from_langchain_documents(
    documents=split_docs,
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1),
    embeddings=embeddings,
    knowledge_graph=kg,
    node_filter=custom_filter  # Use custom filter
)

# Define query distribution
query_distribution = {
    "simple": 0.3,
    "reasoning": 0.3,
    "multi_context": 0.2,
    "conditional": 0.2
}

# Generate testset
print("Generating testset...")
testset = generator.generate(
    testset_size=10, 
    query_distribution=query_distribution,
    num_personas=3  # Reduce number of personas
)

# Convert to pandas and display
df = testset.to_pandas()
print(f"Generated {len(df)} test questions")
print(df.head())

# Save the testset
testset.save("loan_complaints_testset.json")
print("Testset saved to loan_complaints_testset.json") 