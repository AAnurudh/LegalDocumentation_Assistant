import logging
import torch
import chromadb
from chromadb.utils import embedding_functions
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedQAModel:
    def __init__(self, model_name="deepset/roberta-base-squad2", chroma_collection_name="document_collection", 
                 chroma_db_path="./chroma_db"):
        """
        Initialize an improved Question Answering model with RoBERTa that works with ChromaDB
        
        Args:
            model_name (str): Name of the pre-trained model to use
            chroma_collection_name (str): Name of the ChromaDB collection
            chroma_db_path (str): Path to ChromaDB database
        """
        try:
            logger.info(f"Loading QA model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
            
            # Initialize ChromaDB client
            self.chroma_client = chromadb.PersistentClient(path=chroma_db_path)
            
            # Get the collection
            try:
                self.collection = self.chroma_client.get_collection(name=chroma_collection_name)
                logger.info(f"Connected to existing ChromaDB collection: {chroma_collection_name}")
            except ValueError:
                # If collection doesn't exist, create it
                # Using default embedding function (all-MiniLM-L6-v2)
                embedding_function = embedding_functions.DefaultEmbeddingFunction()
                self.collection = self.chroma_client.create_collection(
                    name=chroma_collection_name,
                    embedding_function=embedding_function
                )
                logger.info(f"Created new ChromaDB collection: {chroma_collection_name}")
                
            logger.info(f"QA Model {model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Error initializing QA model: {e}", exc_info=True)
            raise
    
    def retrieve_documents(self, query, top_k=5):
        """
        Retrieve relevant documents from ChromaDB based on the query
        
        Args:
            query (str): The query to search for
            top_k (int): Number of documents to retrieve
            
        Returns:
            list: List of retrieved documents
        """
        try:
            # Query the collection
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # Log the results
            logger.info(f"Retrieved {len(results['documents'][0])} documents for query: {query}")
            
            # Return the documents and their metadata
            documents = []
            for i, doc in enumerate(results['documents'][0]):
                document_data = {
                    'text': doc,
                    'metadata': results.get('metadatas', [[]])[0][i] if results.get('metadatas') else {},
                    'distance': results.get('distances', [[]])[0][i] if results.get('distances') else 0.0,
                    'id': results.get('ids', [[]])[0][i] if results.get('ids') else f"doc_{i}"
                }
                documents.append(document_data)
            
            return documents
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}", exc_info=True)
            return []
    
    def answer_question(self, question, context, max_answer_length=100):
        """
        Generate an answer to a question given the context
        
        Args:
            question (str): The question to answer
            context (str): The context containing the answer
            max_answer_length (int): Maximum length of the answer
            
        Returns:
            dict: The generated answer with confidence score and metadata
        """
        try:
            # Ensure we have valid inputs
            if not context or len(context.strip()) < 5:
                logger.warning("Context is empty or too short")
                return {
                    "answer": "No context provided to answer the question.",
                    "confidence": 0.0,
                    "has_answer": False
                }
            
            # Process context in chunks if it's too long
            max_length = 512  # Maximum sequence length for the model
            
            # Tokenize question once
            question_tokens = self.tokenizer.encode(question, add_special_tokens=False)
            
            # Calculate how many tokens we can use for context
            max_context_tokens = max_length - len(question_tokens) - 3  # 3 for special tokens
            
            # Split context into smaller chunks that fit within token limits
            context_chunks = []
            current_chunk = ""
            current_length = 0
            
            for paragraph in context.split('\n'):
                if not paragraph.strip():
                    continue
                    
                # Tokenize paragraph
                paragraph_tokens = self.tokenizer.encode(paragraph, add_special_tokens=False)
                
                # If adding this paragraph exceeds the limit, save current chunk and start a new one
                if current_length + len(paragraph_tokens) > max_context_tokens and current_chunk:
                    context_chunks.append(current_chunk)
                    current_chunk = paragraph
                    current_length = len(paragraph_tokens)
                else:
                    current_chunk += "\n" + paragraph if current_chunk else paragraph
                    current_length += len(paragraph_tokens)
            
            # Add the last chunk if it exists
            if current_chunk:
                context_chunks.append(current_chunk)
            
            # If we couldn't split by paragraphs, just split by tokens
            if not context_chunks:
                context_tokens = self.tokenizer.encode(context, add_special_tokens=False)
                for i in range(0, len(context_tokens), max_context_tokens):
                    chunk_tokens = context_tokens[i:i + max_context_tokens]
                    chunk_text = self.tokenizer.decode(chunk_tokens)
                    context_chunks.append(chunk_text)
            
            logger.info(f"Split context into {len(context_chunks)} chunks")
            
            # Process each chunk and find the best answer
            best_answer = ""
            best_confidence = float('-inf')
            
            for i, chunk in enumerate(context_chunks):
                logger.info(f"Processing chunk {i+1}/{len(context_chunks)}")
                
                # Tokenize input for this chunk
                inputs = self.tokenizer(
                    question,
                    chunk,
                    add_special_tokens=True,
                    return_tensors="pt",
                    max_length=max_length,
                    truncation=True,
                    padding="max_length"
                )
                
                # Get model output
                with torch.no_grad():
                    outputs = self.model(**inputs)
                
                # Get answer start and end logits
                start_logits = outputs.start_logits[0]
                end_logits = outputs.end_logits[0]
                
                # Get top candidates
                top_k = 10
                start_indexes = torch.topk(start_logits, top_k).indices.tolist()
                end_indexes = torch.topk(end_logits, top_k).indices.tolist()
                
                # Find the best answer in this chunk
                for start_idx in start_indexes:
                    for end_idx in end_indexes:
                        # Skip invalid spans
                        if end_idx < start_idx or end_idx - start_idx + 1 > max_answer_length:
                            continue
                            
                        # Calculate confidence score
                        confidence = float(start_logits[start_idx] + end_logits[end_idx])
                        
                        # Extract answer tokens
                        answer_tokens = inputs.input_ids[0][start_idx:end_idx + 1].tolist()
                        answer_text = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)
                        
                        # Skip empty answers
                        if not answer_text.strip():
                            continue
                            
                        # Update best answer if this one is better
                        if confidence > best_confidence:
                            best_answer = answer_text
                            best_confidence = confidence
            
            # Return the best answer
            if best_answer:
                logger.info(f"Best answer: '{best_answer}' with confidence {best_confidence:.2f}")
                return {
                    "answer": best_answer,
                    "confidence": best_confidence,
                    "has_answer": True
                }
            else:
                logger.warning("No answer found in any chunk")
                return {
                    "answer": "I couldn't find an answer to your question in the provided documents.",
                    "confidence": 0.0,
                    "has_answer": False
                }
                
        except Exception as e:
            logger.error(f"Error in answer generation: {e}", exc_info=True)
            return {
                "answer": f"Error processing your question: {str(e)}",
                "confidence": 0.0,
                "has_answer": False
            }
    
    def process_query(self, query, use_retrieved_docs=True, provided_docs=None):
        """
        End-to-end processing of a query
        
        Args:
            query (str): The user's question
            use_retrieved_docs (bool): Whether to retrieve documents or use provided ones
            provided_docs (list): Optional list of documents to use instead of retrieving
            
        Returns:
            dict: Answer information
        """
        try:
            # Get documents
            if use_retrieved_docs:
                documents = self.retrieve_documents(query)
            else:
                documents = provided_docs or []
            
            # Ensure we have documents
            if not documents:
                logger.warning("No documents available")
                return {
                    "answer": "No relevant documents found to answer your question.",
                    "confidence": 0.0,
                    "has_answer": False
                }
            
            # Extract text from documents
            all_text = []
            for doc in documents:
                if isinstance(doc, dict) and 'text' in doc:
                    all_text.append(doc['text'])
                elif isinstance(doc, str):
                    all_text.append(doc)
                else:
                    try:
                        # Try to convert to string
                        all_text.append(str(doc))
                    except:
                        logger.warning(f"Couldn't extract text from: {type(doc)}")
            
            # Combine all text
            combined_text = "\n\n".join(all_text)
            
            # Generate answer
            result = self.answer_question(query, combined_text)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in query processing: {e}", exc_info=True)
            return {
                "answer": f"Error processing your query: {str(e)}",
                "confidence": 0.0,
                "has_answer": False
            }