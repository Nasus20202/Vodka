from pathlib import Path
import sys
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

if len(sys.argv) > 1:
    token = sys.argv[1]

user_metadata_path = Path("./data/user_metadata.json")
