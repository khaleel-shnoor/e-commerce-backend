"""
Embeddings pipeline (Phase 4).

Planned:
- Product title/description → embedding via external model API
- Storage in PostgreSQL pgvector column (product_embeddings table)
- Batch jobs in app/jobs for catalog re-indexing
- Versioning for model upgrades (embedding_model_id column)
"""
