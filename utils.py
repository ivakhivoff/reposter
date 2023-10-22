import random
from typing import Iterator
from config import (
    ACCOUNT_FOLDER,
    API_HASH,
    API_ID,
    MESSAGES,
    PHOTO_FOLDER,
    PROXY_FILE,
    PROXY_IPV6,
    USE_PROXY,
)
from telethon.sync import TelegramClient
from itertools import cycle
import os
import python_socks


def readlines(filename: str):
    with open(filename, encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]


def proxy_gen():
    for proxy in readlines(PROXY_FILE):
        proxy = proxy.split(":")
        yield {
            "proxy_type": python_socks.ProxyType.SOCKS5,
            "addr": proxy[0],
            "port": int(proxy[1]),
            "username": proxy[2],
            "password": proxy[3],
        }


if USE_PROXY:
    proxys = cycle(list(proxy_gen()))


def get_client(session):
    if USE_PROXY:
        client = TelegramClient(
            session, API_ID, API_HASH, proxy=next(proxys), use_ipv6=PROXY_IPV6
        )
    else:
        client = TelegramClient(
            session,
            API_ID,
            API_HASH,
        )
    client.connect()

    return client


def get_accounts():
    accounts = []
    for session in os.listdir(ACCOUNT_FOLDER):
        try:
            client = get_client(os.path.join(ACCOUNT_FOLDER, session))
            is_authorized = client.is_user_authorized()
            print(f"[{session}] Authorized: {is_authorized}")
            if is_authorized:
                accounts.append(client)
        except Exception as e:
            print(f"[ERROR] {session}: {e.__class__.__name__} - {e}")

    print(len(accounts))
    return accounts


def get_random_msg_text():
    return random.choice(MESSAGES)


def get_random_img():
    filenames = os.listdir(PHOTO_FOLDER)
    random_file = random.choice(filenames)
    return f"{PHOTO_FOLDER}/{random_file}"


def accounts_gen() -> Iterator[TelegramClient]:
    accounts = get_accounts()
    yield from accounts
