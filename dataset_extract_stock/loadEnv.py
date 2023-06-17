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
    return os.getenv(varenv)
