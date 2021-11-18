from typing import List, Set
from pyrogram.client import Client
import logging
import random
from pyrogram.methods.chats.get_chat_members import Filters
from pyrogram.types.user_and_chats import user

from pyrogram.types.user_and_chats.chat_member import ChatMember

def ch_mem_hashable(self: ChatMember):
    return hash(self.user.id)

ChatMember.__hash__ = ch_mem_hashable

class Selector:
    PAGE_SIZE: int = 100

    def __init__(self, app: Client, chat_id: int):
        self.app = app
        self.chat_id = chat_id

    async def get_admin_members(self) -> List[ChatMember]:
        return await self.app.get_chat_members(
            self.chat_id, filter=Filters.ADMINISTRATORS
        )

    async def get_members(self) -> Set[ChatMember]:
        count: int = await self.app.get_chat_members_count(self.chat_id)

        print(f"There are {count} members in chat with id {self.chat_id}")

        members_set: Set[ChatMember] = set()
        pages = count // self.PAGE_SIZE + ((count % self.PAGE_SIZE) != 0)

        for page in range(pages):
            members_set =  members_set.union(set(
                await self.app.get_chat_members(
                    self.chat_id, page, self.PAGE_SIZE, "", Filters.ALL
                )
            ))
        return members_set


class MsgDecs:
    PAGE_SIZE: int = 20

    @staticmethod
    def filter_members(members: List[ChatMember]) -> List[ChatMember]:
        return list(member for member in members if member.status == "member")

    @staticmethod
    def list_view_as_md(members: List[ChatMember]) -> List[str]:
        i, chunks = 1, []

        user_def_str = ""

        for member in members:
            user_def_str = user_def_str + "\n" + f"{i}. {member.user.mention()}"
            if i % MsgDecs.PAGE_SIZE == 0:
                chunks.append(user_def_str)
                user_def_str = ""

            i += 1
        if user_def_str != "":
            chunks.append(user_def_str)

        return chunks

    @staticmethod
    def choose_one_from(members: List[ChatMember]) -> ChatMember:
        return members[random.randint(0, len(members)-1)]

    @staticmethod
    def aqalay_maqalay() -> str:
        return "Aqalay-Maqalay!\n"

    @staticmethod
    def down_counter(start: int):
        return (i for i in range(start, 0, -1))

    @staticmethod
    def decorate_winner(member: ChatMember) -> str:
        return f"The most anticipated owner, {member.user.mention()}, happy new T!\n"
