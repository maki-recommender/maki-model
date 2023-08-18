import os
import logging
import sys

def env_var(name: str, default_value = None,):
    """Get environment variable with a default value

    Args:
        name: env variable to search
        default_value: given default value for the variable
    
    Returns: 
        Variable value or the default value if provided.
        If no default value is provided the application is crashed
    """
    if name in os.environ:
        return os.environ[name]
    elif default_value is not None:
        logging.info("Using fallback env for %s", name)
        return default_value
    
    logging.critical("Missing env var %s", name)
    sys.exit(5)