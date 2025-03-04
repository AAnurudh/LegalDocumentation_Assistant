import logging
from document_embedding import collection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def retrieve_documents(query, top_k=5, similarity_threshold=0.7):
    """
    Retrieve relevant documents based on a query using vector similarity search
    
    Args:
        query (str): The query text
        top_k (int): Maximum number of documents to retrieve
        similarity_threshold (float): Threshold for similarity score (0-1, higher means more similar)
        
    Returns:
        dict: Results containing matches with document content and metadata
    """
    if not query:
        logger.warning("Empty query provided")
        return {"matches": []}
    
    logger.info(f"Retrieving documents for query: {query}")
    
    try:
        # Query ChromaDB collection
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        if not results or 'documents' not in results or not results['documents'] or not results['documents'][0]:
            logger.warning("No documents found for the query")
            return {"matches": []}
        
        # Format results for easier consumption and filter by similarity
        matches = []
        for i, doc_id in enumerate(results['ids'][0]):
            # Skip if we have distances and it's below our threshold
            # ChromaDB distance is smaller for more similar docs, so we invert
            if 'distances' in results and i < len(results['distances'][0]):
                # Convert distance to similarity score (0-1)
                # ChromaDB cosine distance is 1-cosine_similarity
                similarity = 1 - results['distances'][0][i]
                if similarity < similarity_threshold:
                    logger.info(f"Skipping document {doc_id} with similarity {similarity:.4f} (below threshold {similarity_threshold})")
                    continue
            
            doc_text = results['documents'][0][i]
            doc_metadata = results['metadatas'][0][i] if 'metadatas' in results and results['metadatas'] and i < len(results['metadatas'][0]) else {}
            
            # Make sure we have the text in a consistent place
            if not doc_text and 'text' in doc_metadata:
                doc_text = doc_metadata['text']
            
            # Calculate relevance score (inverted distance, higher is better)
            relevance = 1 - results['distances'][0][i] if 'distances' in results and i < len(results['distances'][0]) else 0
            
            # Log the first 100 chars of each retrieved document for debugging
            logger.info(f"Retrieved doc {i+1}: {doc_text[:100]}... (similarity: {relevance:.4f})")
            
            matches.append({
                'id': doc_id,
                'text': doc_text,
                'metadata': doc_metadata,
                'similarity': relevance,
                'raw_distance': results['distances'][0][i] if 'distances' in results and i < len(results['distances'][0]) else None
            })
        
        # Sort matches by similarity score (highest first)
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        
        logger.info(f"Retrieved {len(matches)} documents for query: '{query}'")
        return {"matches": matches}
        
    except Exception as e:
        logger.error(f"Error during document retrieval: {e}")
        return {"matches": [], "error": str(e)}

def retrieve_document_by_id(doc_id):
    """
    Retrieve a specific document by ID
    
    Args:
        doc_id (str): The document ID
        
    Returns:
        dict: Document content and metadata
    """
    try:
        result = collection.get(ids=[doc_id])
        
        if not result or 'documents' not in result or not result['documents']:
            logger.warning(f"Document with ID {doc_id} not found")
            return None
        
        document = {
            'id': doc_id,
            'text': result['documents'][0],
            'metadata': result['metadatas'][0] if 'metadatas' in result and result['metadatas'] else {}
        }
        
        return document
    except Exception as e:
        logger.error(f"Error retrieving document {doc_id}: {e}")
        return None