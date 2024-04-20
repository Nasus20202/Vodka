import sys
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")
channel_id = int(os.getenv("CHANNEL_ID"))

if len(sys.argv) > 1:
    token = sys.argv[1]
