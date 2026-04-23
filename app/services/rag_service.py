import os
import pandas as pd
import chromadb
from chromadb.config import Settings
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Abstracting the DB layer so we can swap to Pinecone/Supabase for production
class VectorDBProvider:
    def __init__(self):
        # We use a local persistent directory right now.
        # When deploying to Railway/HuggingFace, this should be mounted as a Volume, 
        # or we swap this class for a Pinecone implementation.
        self.persist_directory = os.path.join(os.getcwd(), "chroma_data")
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # We will use the default Sentence-Transformers embedding model provided by Chroma
        self.collection = self.client.get_or_create_collection(name="travel_knowledge_base")
        logger.info(f"Initialized Vector DB. Collection count: {self.collection.count()}")

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, str]], ids: List[str]):
        """Inject vector data into the knowledge base."""
        # Process in batches to avoid overwhelming memory
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            self.collection.add(
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size]
            )

    def query(self, query_texts: List[str], n_results: int = 5) -> List[Dict[str, Any]]:
        """Search the knowledge base"""
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
        return results

class RAGService:
    def __init__(self):
        self.db = VectorDBProvider()
        
    def _create_summary_from_row(self, row: pd.Series) -> str:
        """Convert a row of raw CSV stats into a rich semantic paragraph for the LLM."""
        city = row.get("city", "Unknown")
        country = row.get("country", "Unknown")
        
        # Map some common keys to human readable form
        # We rely on typical Cost of Living index shapes (e.g., x1 = Meal, Inexpensive Restaurant)
        # For simplicity, we just dump the core metadata into a clean readable string.
        stats = []
        for key, value in row.items():
            if key not in ['city', 'country', 'data_quality'] and pd.notna(value):
                stats.append(f"Metric {key}: {value}")
                
        stat_summary = ", ".join(stats)
        
        return f"Regarding the cost of living and travel expenses in {city}, {country}: {stat_summary}. This data provides excellent budget context."

    def ingest_cost_of_living_data(self, csv_path: str):
        """Read the CSV and dump it into the Vector Database. Run this once on startup."""
        if not os.path.exists(csv_path):
            logger.error(f"Dataset not found at {csv_path}")
            return
            
        # Check if already ingested to avoid duplicates in local storage
        if self.db.collection.count() > 0:
            logger.info("Database already populated. Skipping ingestion to save time.")
            return

        logger.info("Initializing massive data ingestion into Vector DB. This may take a minute...")
        try:
            df = pd.read_csv(csv_path)
            
            docs = []
            metadatas = []
            ids = []
            
            for index, row in df.iterrows():
                city = str(row.get("city", ""))
                country = str(row.get("country", ""))
                
                # Protect against bad data
                if not city or not country:
                    continue
                    
                doc_text = self._create_summary_from_row(row)
                
                docs.append(doc_text)
                metadatas.append({"city": city, "country": country, "source": "cost_of_living_db"})
                ids.append(f"col_{city.replace(' ', '_').lower()}_{index}")
            
            # Write to database
            self.db.add_documents(docs, metadatas, ids)
            logger.info(f"Successfully processed {len(docs)} locations into the RAG brain.")
            
        except Exception as e:
            logger.error(f"Failed to ingest CSV: {e}")

    def query_local_context(self, search_query: str) -> str:
        """The actual method called by the AI Tool."""
        logger.info(f"Triggering RAG search for: {search_query}")
        results = self.db.query(query_texts=[search_query], n_results=3)
        
        if not results['documents'] or not results['documents'][0]:
            return "No specific local knowledge found for this query."
            
        # Join the top hits into a context block
        context_block = "\n---\n".join(results['documents'][0])
        return f"Local Pricing Context found:\n{context_block}"

rag_service = RAGService()
