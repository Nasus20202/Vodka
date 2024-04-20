from __future__ import annotations
import discord
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ListUser:
    discord_user: discord.User
    attending: bool = None
    enlisted: bool = False
    enlister: discord.User = None
    enlist_time: datetime = None
    sleeping_until: datetime = None
    name: str = None
    index_number: int = None

    def reset(self) -> None:
        self.attending = None
        self.enlisted = False
        self.enlister = None
        self.enlist_time = None

    def __str__(self):
        return self.name if self.name else self.discord_user.display_name


class ListManager:
    def __init__(self):
        self.users: dict[int, ListUser] = {}

    def set_user_attending(self, user: discord.User, attending: bool) -> None:
        if user.id not in self.users:
            self.users[user.id] = ListUser(user)
        self.users[user.id].attending = attending

    def enlist_user(self, user: discord.User, enlister: discord.User) -> None:
        if user.id not in self.users:
            self.users[user.id] = ListUser(user)

        self.users[user.id].enlisted = True
        self.users[user.id].enlister = enlister
        self.users[user.id].enlist_time = datetime.now()

        if enlister.id not in self.users:
            self.users[enlister.id] = ListUser(enlister)
        self.users[enlister.id].attending = True

    def reset_list(self) -> None:
        for user in self.users:
            self.users[user].reset()

    def sleep_user(self, user: discord.User, duration: datetime.timedelta) -> None:
        if user.id not in self.users:
            self.users[user.id] = ListUser(user)
        self.users[user.id].sleeping_until = datetime.now() + duration

    def set_user_metadata(
        self, user: discord.User, name: str, index_number: str
    ) -> None:
        if user.id not in self.users:
            self.users[user.id] = ListUser(user)

        self.users[user.id].name = name
        self.users[user.id].index_number = index_number

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
        
