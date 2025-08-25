"""
Embedding generation using Hugging Face Transformers (no sentence-transformers, no Rust).
"""

from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        self.model = AutoModel.from_pretrained(model_name)
        logger.info(f"Loaded Hugging Face model: {model_name}")

    def embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        embeddings = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Mean pooling
                emb = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
                embeddings.append(emb)
        return np.vstack(embeddings)

if __name__ == "__main__":
    embedder = HuggingFaceEmbedder()
    texts = ["This is a test.", "Another sentence."]
    embs = embedder.embed(texts)
    print(embs.shape)
    print(embs) 