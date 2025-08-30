import logging
import yaml
import hashlib
import random
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
    

def get_unique_id(topic, user_content_dict):
    try:
        user_content_str = str(user_content_dict) if user_content_dict else ""
        unique_string = f"{topic}_{user_content_str}"
        unique_id = hashlib.md5(unique_string.encode()).hexdigest()
        return unique_id
    
    except Exception as e:
        logger.error(f"Error generating unique ID: {e}")
        return str(random.randint(100000, 999999))
    

def prepare_output_json(status, tts_output_path_dict, error_message = ""):
    return {"status": status, "tts_output_path": tts_output_path_dict, "error_message": error_message}
        