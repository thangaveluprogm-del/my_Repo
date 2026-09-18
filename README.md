# my_Repo
small capstone project
installing !pip install -qU langchain langchain-community langchain-core langchain-text-splitters chromadb sentence-transformers pypdf unstructured
after then Embedding model initialized: all-MiniLM-L6-v2

Excellent! The LangGraph is now fully functional and correctly handling intent classification and question answering. All test queries executed successfully, and the answers are being returned in the specified JSON format, complete with the answer text, document sources, and confidence scores. This confirms that all previous errors have been resolved and the output schema is being enforced.


# Use a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and data
COPY MOCK_LLM.ipynb .
COPY docs/ ./docs/
COPY chroma_db/ ./chroma_db/

# Expose the port FastAPI will run on
EXPOSE 8080

# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "120.0.0.8", "--port", "8080"]



Demonstration of FastAPI Calls

To run the FastAPI application:

Build the Docker image:
docker build -t zepto-rag-app .
Run the Docker container:
docker run -p 7860:7860 zepto-rag-app
Once the application is running, you can make POST requests to the /ask endpoint.

Example 1: Policy Question (Triggers Retrieval)
curl command:

curl -X POST "http://localhost:8080/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "How do I get a refund for a damaged item?"}'
Expected JSON Response:

{
  "answer": "Based on the retrieved context: Returns & Refunds: \"Grocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect; non-perishable packaged items may be returned within 7 days...",
  "sources": [
    "docs/doc_02.txt",
    "docs/doc_06.txt",
    "docs/doc_02.txt"
  ],
  "confidence": 1.0
}
Example 2: General Question (Does Not Trigger Retrieval)
curl command:

curl -X POST "http://localhost:8080/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the capital of France?"}'
Expected JSON Response:

{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
