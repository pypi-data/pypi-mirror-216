# Utils to load env variables and set up logging
from dotenv import load_dotenv
import logging
import yaml
import os

VARS_FULL_PATH = "/Users/croft/VScode/ptagit/env_vars.yaml"
LOG_FORMAT = "%(levelname)s [function: %(funcName)s] - %(message)s"

def setup_logger(logger_name, log_level=logging.INFO, log_format=LOG_FORMAT):
    """ returns a logger instance. creates a handler automaticaly if name == '__main__' """
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # add console handler with custom format if running standalone
    if logger_name == '__main__':
        console_handler = logging.StreamHandler()        
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def load_dotenv_file(path = "../.env"):
    load_dotenv(dotenv_path=path)

def load_env_variables_from_yaml(full_path_file_name=VARS_FULL_PATH):    
    if hasattr(load_env_variables_from_yaml, "has_run"):
        return
    try:
        with open(full_path_file_name, 'r') as stream:
            params = yaml.safe_load(stream)
            for key, value in params.items():
                value = str(value) 
                os.environ[key] = value
        # set this attribute so don't keep running the function in the same program
        load_env_variables_from_yaml.has_run = True
    except FileNotFoundError:
        pass  # Ignore the file not found error as it is expected in some environments
            
    
