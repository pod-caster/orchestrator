import os
import yaml
from types import SimpleNamespace

def load_yaml_files_as_namespace(folder_path):
    yaml_namespace = SimpleNamespace()
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.yaml', '.yml')):
            key_name = os.path.splitext(file_name)[0]
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    yaml_data = yaml.safe_load(f)
                    setattr(yaml_namespace, key_name, yaml_data)
                except yaml.YAMLError as e:
                    print(f"Error parsing {file_name}: {e}")
    return yaml_namespace