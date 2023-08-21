"""
Aims to allow getting environment variables from .env file
"""

# Import Packages
from dotenv import load_dotenv
import os

def loadEnv(varenv:str):
    """load environment variable

    Args:
        varenv (str): environment variable name

    Returns:
        string: env var value
    """
    load_dotenv() # CHARGE LE FICHIER .env
    mystring = str(os.getenv(varenv))
    return mystring
