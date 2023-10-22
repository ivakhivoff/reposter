import os
from telethon.sync import TelegramClient
import time
import traceback
from config import ACCOUNT_FOLDER, API_HASH, API_ID


def create_client():
    phone_number = input("Phone number: ")
    client = TelegramClient(os.path.join(ACCOUNT_FOLDER, phone_number), API_ID, API_HASH)

    client.start(phone_number)


while True:
    try:
        create_client()
    except Exception as e:
        print("Error: ", traceback.format_exc())
