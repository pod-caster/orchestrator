import logging
import yaml
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def convert_input_to_dict(input):
    try:
        return input.dict()
    
    except Exception as e:
        logger.error(f"Error converting input to dict: {e}")
        return input

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error loading YAML config from {file_path}: {e}")
        return None
    

    