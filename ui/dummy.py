import os
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent

def dummy(input_dict):
    time.sleep(30)  # Simulate a delay
    return {"tts_output_path":[{"episode_name" : "Ethical and Societal Implications of AI","episode_path" : f"{BASE_DIR}/output/2296_Ethical_and_Societal_Implications.wav"},{"episode_name" : "AI's Transformative Applications","episode_path" : f"{BASE_DIR}/output/7421_AI's_Transformative_Applications.wav"},
            {"episode_name" : "AI's Potential","episode_path" : f"{BASE_DIR}/output/9828_AI's_Potential.wav"}]}