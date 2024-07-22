import os
import sys
from dotenv import load_dotenv

env_path = os.path.join(sys.path[0], ".env")
load_dotenv(env_path)

class RM_Settings():
    RM_USER: str = os.getenv("RM_USER")
    RM_PASSWORD: str = os.getenv("RM_PASSWORD")
    RM_HOST: str = os.getenv("RM_HOST")
    RM_PORT: int = os.getenv("RM_PORT", "5672")
