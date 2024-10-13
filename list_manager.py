from __future__ import annotations
import discord
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ListUserMetadata:
    name: str = None
    index_number: int = None


@dataclass
class ListUser:
    discord_user: discord.User
    attending: bool = None
    enlisted: bool = None
    enlister: discord.User = None
    enlist_time: datetime = None
    sleeping_until: datetime = None
    metadata: ListUserMetadata = field(default_factory=ListUserMetadata)

    def reset(self) -> None:
        self.attending = None
        self.enlisted = None
        self.enlister = None
        self.enlist_time = None

    def __str__(self):
        return (
            self.metadata.name
            if self.metadata and self.metadata.name
            else self.discord_user.display_name
        )


class ListManager:
    def __init__(self):
        self.users: dict[int, ListUser] = {}

    def ensure_list_user(self, user: discord.User) -> None:
        if user.id not in self.users:
            self.users[user.id] = ListUser(user)
        elif self.users[user.id].discord_user is None:
            self.users[user.id].discord_user = user

    def set_user_attending(self, user: discord.User, attending: bool) -> None:
        self.ensure_list_user(user)
        self.users[user.id].attending = attending

    def enlist_user(self, user: discord.User, enlister: discord.User) -> None:
        self.ensure_list_user(user)

        self.users[user.id].enlisted = True
        self.users[user.id].enlister = enlister
        self.users[user.id].enlist_time = datetime.now()

        self.ensure_list_user(enlister)
        self.users[enlister.id].attending = True

    def reset_list(self) -> None:
        for user in self.users:
            self.users[user].reset()

    def sleep_user(self, user: discord.User, duration: datetime.timedelta) -> None:
        self.ensure_list_user(user)
        self.users[user.id].sleeping_until = datetime.now() + duration

    def set_user_metadata(
        self, user: discord.User, name: str, index_number: str
    ) -> None:
        self.ensure_list_user(user)
        self.users[user.id].metadata = ListUserMetadata(name, index_number)

    def get_all_users(self) -> list[ListUser]:
        return [self.users[user] for user in self.users]

    def get_not_enlisted(self) -> list[ListUser]:
        return [user for user in self.users if not self.users[user].enlisted]

    def get_enlisted(self) -> list[ListUser]:
        return [self.users[user] for user in self.users if self.users[user].enlisted]

    def get_not_attending(self) -> list[ListUser]:
        return [
            self.users[user]
            for user in self.users
            if (
                self.users[user].attending is False
                or (
                    self.users[user].sleeping_until is not None
                    and self.users[user].sleeping_until >= datetime.now()
                )
            )
            and self.users[user].enlister is None
        ]
