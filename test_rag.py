import asyncio
from app.services.rag_service import rag_service
import os
import sys

async def test_rag():
    csv_path = os.path.join(os.getcwd(), "app/services", "cost_of_living_dataset.csv")    
    print("Starting ingestion...")
    rag_service.ingest_cost_of_living_data(csv_path)
    print("Ingestion complete.")
    
    print("Testing query...")
    result = rag_service.query_local_context("cost of living in Seoul")
    print("\nQUERY RESULT:")
    print(result)

if __name__ == "__main__":
    asyncio.run(test_rag())
