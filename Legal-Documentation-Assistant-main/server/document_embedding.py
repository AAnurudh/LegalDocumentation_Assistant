import os
import logging
import chromadb
from chromadb.utils import embedding_functions

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize ChromaDB client
try:
    client = chromadb.PersistentClient(path="./chroma_db")
    logger.info("Connected to ChromaDB")
except Exception as e:
    logger.error(f"Error connecting to ChromaDB: {e}")
    raise

# Create or get collection with default embedding function
try:
    # Use ChromaDB's built-in DefaultEmbeddingFunction (which uses all-MiniLM-L6-v2)
    embedding_function = embedding_functions.DefaultEmbeddingFunction()
    
    collection = client.get_or_create_collection(
        name="document_collection",
        embedding_function=embedding_function,
        metadata={"description": "Collection for document retrieval system"}
    )
    logger.info("Collection initialized with default embedding function")
except Exception as e:
    logger.error(f"Error creating collection: {e}")
    raise

def upsert_embeddings(texts, metadatas=None, ids=None):
    """
    Add documents to the ChromaDB collection
    
    Args:
        texts (list): List of text documents
        metadatas (list, optional): List of metadata dictionaries
        ids (list, optional): List of document IDs
        
    Returns:
        bool: Success status
    """
    if not texts:
        logger.warning("No texts provided for embedding")
        return False
    
    if not ids:
        logger.warning("No IDs provided, generating sequential IDs")
        ids = [f"doc_{i}" for i in range(len(texts))]
    
    if not metadatas:
        metadatas = [{"source": "unknown"} for _ in range(len(texts))]
    
    try:
        # Add documents to collection - ChromaDB will handle the embedding conversion
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Successfully added {len(texts)} documents to collection")
        return True
    except Exception as e:
        logger.error(f"Error upserting embeddings: {e}")
        return False

def query_by_text(query_text, top_k=5):
    """
    Query the collection using text
    
    Args:
        query_text (str): The query text
        top_k (int): Number of results to return
        
    Returns:
        dict: Query results
    """
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        logger.info(f"Query executed successfully for: '{query_text}'")
        return results
    except Exception as e:
        logger.error(f"Error querying collection: {e}")
        return None

def delete_document(doc_id):
    """
    Delete a document from the collection
    
    Args:
        doc_id (str): Document ID to delete
        
    Returns:
        bool: Success status
    """
    try:
        collection.delete(ids=[doc_id])
        logger.info(f"Document {doc_id} deleted successfully")
        return True
    except Exception as e:
        logger.error(f"Error deleting document {doc_id}: {e}")
        return False

def get_document_count():
    """
    Get the number of documents in the collection
    
    Returns:
        int: Number of documents
    """
    try:
        # Get collection info
        info = collection.count()
        return info
    except Exception as e:
        logger.error(f"Error getting document count: {e}")
        return 0

# For testing the module
if __name__ == "__main__":
    # Test adding documents
    print("Testing document insertion...")
    test_texts = [
        "This is a test document about machine learning",
        "This is another test document about natural language processing"
    ]
    
    success = upsert_embeddings(
        texts=test_texts,
        metadatas=[{"source": "test", "content_type": "text"} for _ in test_texts],
        ids=[f"test_{i}" for i in range(len(test_texts))]
    )
    
    print(f"Document insertion successful: {success}")
    
    # Test query
    print("Testing querying...")
    results = query_by_text("machine learning")
    
    if results and 'documents' in results and results['documents']:
        print(f"Found {len(results['documents'][0])} documents")
        for i, doc in enumerate(results['documents'][0]):
            print(f"Document {i+1}: {doc[:100]}...")
            print(f"Distance: {results['distances'][0][i]}")
    else:
        print("No results found")