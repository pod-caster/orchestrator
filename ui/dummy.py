import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def dummy(input_dict):
    return [{"episode_title" : "Ethical and Societal Implications of AI","episode_path" : f"{BASE_DIR}/output/2296_Ethical_and_Societal_Implications.wav"},{"episode_title" : "AI's Transformative Applications","episode_path" : f"{BASE_DIR}/output/7421_AI's_Transformative_Applications.wav"},
            {"episode_title" : "AI's Potential","episode_path" : f"{BASE_DIR}/output/9828_AI's_Potential.wav"}]