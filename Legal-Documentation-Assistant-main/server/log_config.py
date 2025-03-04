import logging
import json
import time
import os
from functools import wraps
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('./logs'):
    os.makedirs('./logs')

# Configure main logger
logger = logging.getLogger('document_qa')
logger.setLevel(logging.DEBUG)

# Create console handler with formatting
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# Create file handler for detailed logs
file_handler = logging.FileHandler('./logs/docqa_app.log')
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

# Create a separate file handler for data flow logging
data_logger = logging.getLogger('data_flow')
data_logger.setLevel(logging.DEBUG)
data_file_handler = logging.FileHandler('./logs/data_flow.log')
data_file_handler.setLevel(logging.DEBUG)
data_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
data_logger.addHandler(data_file_handler)

def log_function_call(func):
    """Decorator to log function calls with parameters and return values"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        module_name = func.__module__
        
        # Log function entry with safe parameter logging
        safe_args = [f"{arg:.100}..." if isinstance(arg, str) and len(arg) > 100 else arg for arg in args]
        safe_kwargs = {k: f"{v:.100}..." if isinstance(v, str) and len(v) > 100 else v for k, v in kwargs.items()}
        
        logger.debug(f"ENTER: {module_name}.{func_name} - args: {safe_args}, kwargs: {safe_kwargs}")
        
        # Measure execution time
        start_time = time.time()
        
        try:
            # Call the original function
            result = func(*args, **kwargs)
            
            # Calculate execution time
            exec_time = time.time() - start_time
            
            # Log function exit with safe result logging
            if isinstance(result, str) and len(result) > 100:
                safe_result = f"{result[:100]}..."
            elif isinstance(result, dict):
                # Handle common dict case and redact potentially sensitive content
                safe_result = {}
                for k, v in result.items():
                    if isinstance(v, str) and len(v) > 100:
                        safe_result[k] = f"{v[:50]}..."
                    else:
                        safe_result[k] = v
            else:
                safe_result = result
                
            logger.debug(f"EXIT: {module_name}.{func_name} - execution time: {exec_time:.4f}s - result: {safe_result}")
            
            return result
            
        except Exception as e:
            # Log exception details
            exec_time = time.time() - start_time
            logger.error(f"EXCEPTION in {module_name}.{func_name}: {str(e)} - execution time: {exec_time:.4f}s")
            raise
            
    return wrapper

def log_data_flow(data_type, content, source=None, destination=None):
    """
    Log data as it flows between components
    
    Args:
        data_type (str): Type of data being logged (e.g., 'query', 'document', 'response')
        content: The data content
        source (str): Source component
        destination (str): Destination component
    """
    try:
        # Create entry with metadata
        entry = {
            'timestamp': datetime.now().isoformat(),
            'data_type': data_type,
            'source': source,
            'destination': destination
        }
        
        # Add content preview based on type
        if isinstance(content, str):
            if len(content) > 200:
                entry['content_preview'] = content[:200] + '...'
                entry['content_length'] = len(content)
            else:
                entry['content_preview'] = content
        elif isinstance(content, dict):
            entry['content_keys'] = list(content.keys())
            # Add brief preview of values
            preview = {}
            for k, v in content.items():
                if isinstance(v, str):
                    preview[k] = v[:50] + '...' if len(v) > 50 else v
                else:
                    preview[k] = str(type(v))
            entry['content_preview'] = preview
        elif isinstance(content, list):
            entry['content_length'] = len(content)
            entry['content_preview'] = f"List with {len(content)} items"
            if content and len(content) > 0:
                entry['first_item_type'] = str(type(content[0]))
        else:
            entry['content_type'] = str(type(content))
        
        # Log the entry
        data_logger.info(json.dumps(entry))
    except Exception as e:
        logger.error(f"Error logging data flow: {e}")