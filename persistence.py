from config import *
from list_manager import ListManager, ListUserMetadata, ListUser
import json
from pathlib import Path


def backup_user_metadata(manager: ListManager) -> None:
    Path(user_metadata_path).parent.mkdir(parents=True, exist_ok=True)

    user_metadata = {}
    for key, list_user in manager.users.items():
        if list_user.metadata is not None:
            user_metadata[key] = list_user.metadata
    with open(user_metadata_path, "w") as file:
        json.dump(user_metadata, file, default=lambda o: o.__dict__)


def load_user_metadata(manager: ListManager) -> ListManager:
    if not Path(user_metadata_path).exists():
        return manager

    with open(user_metadata_path, "r") as file:
        backup_data = json.load(file)

    for key, metadata in backup_data.items():
        key = int(key)
        if key not in manager.users:
            manager.users[key] = ListUser(None)
        manager.users[key].metadata = ListUserMetadata(**metadata)

    return manager
