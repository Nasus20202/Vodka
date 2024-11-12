from pathlib import Path
import sys
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

if len(sys.argv) > 1:
    token = sys.argv[1]

user_metadata_path = Path("./data/user_metadata.json")

# List of default better users (ketrab20, Nasus, KanarekLife)
better_users = (
    os.getenv("BETTER_USERS").split(",")
    if os.getenv("BETTER_USERS")
    else [374952720295133184, 374952720295133184, 296347644081471502]
)
