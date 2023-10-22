import asyncio
import os
import traceback
from telethon import TelegramClient, events
from config import DESTINATION, API_ID, API_HASH, SESSION, CHATS, KEY_WORDS
from telethon.tl.functions.channels import (
    InviteToChannelRequest,
    GetParticipantsRequest,
)
from telethon.tl.functions.messages import (
    ImportChatInviteRequest,
    AddChatUserRequest,
    CheckChatInviteRequest,
)
from telethon.errors.rpcerrorlist import (
    FloodWaitError,
    PeerFloodError,
    UsernameNotOccupiedError,
    UserRestrictedError,
    UserBannedInChannelError,
    UserPrivacyRestrictedError,
    UserNotMutualContactError,
    ChatAdminRequiredError,
    UserAlreadyParticipantError,
    UserChannelsTooMuchError,
    UsernameInvalidError,
    UserIdInvalidError,
    InputUserDeactivatedError,
    ChannelsTooMuchError,
)

from telethon.types import ChatInviteAlready, ChannelParticipantsSearch
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.functions.channels import JoinChannelRequest


async def join_chat(acc: TelegramClient, link: str):
    link_hash = link.lstrip("@")
    try:
        ent = await acc(JoinChannelRequest(link_hash))
    except (FloodWaitError) as e:
        print(f"[{link}] [{acc.session.filename}] Флуд еррор, ожидание {e.seconds}")
        await asyncio.sleep(e.seconds)
    except:
        print(f"[{link}] [{acc.session.filename}] Другая ошибка при входе в чат")
        print(traceback.format_exc())
        return "not_join"
    print(f"{acc.session.filename} присоединился к чату {link}")
    await asyncio.sleep(5)
    return ent


async def main():
    print("Program is running...")

    for file in SESSION:
        # if not file.endswith(".session"):
        #     continue
        # filepath = os.path.join("accs", file)
        try:
            client = TelegramClient(file, API_ID, API_HASH)

            await client.connect()
            if not await client.is_user_authorized():
                print(file, "not auth")
                await client.disconnect()
                continue

            @client.on(events.NewMessage(chats=CHATS))
            async def new_order(event):
                try:
                    print("Delivery new order...")
                    contain_key_word = False

                    for key_word in KEY_WORDS:
                        if key_word in event.message.message:
                            contain_key_word = True

                    if contain_key_word:
                        await client.forward_messages(DESTINATION, event.message)

                except Exception as ex:
                    print(f"Exception: {ex}")

            chat_names = set()
            from telethon.types import Chat, Channel

            async for dialog in client.iter_dialogs():
                try:
                    if dialog.entity.megagroup:
                        chat_names.add(dialog.entity.username)
                except:
                    pass
            for chat in CHATS:
                chat = chat.lstrip("@")
                if chat in chat_names:
                    continue
                print(f"Join chat {chat}")
                try:
                    await join_chat(client, chat)
                except:
                    print("ошибка присоединения к группе, след. группа")
                    print(traceback.format_exc())
                await asyncio.sleep(10)
            await client.run_until_disconnected()
        except:
            print("error, next account")
            print(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
