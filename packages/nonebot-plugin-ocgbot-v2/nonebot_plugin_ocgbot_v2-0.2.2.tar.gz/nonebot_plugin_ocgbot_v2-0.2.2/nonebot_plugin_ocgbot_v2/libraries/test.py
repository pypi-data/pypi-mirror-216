import asyncio
import json
import os
import re

import httpx
deck_url = "https://raw.githubusercontent.com/fireinsect/imageSave/master/deck/"
deck_path="F:/CodeProject/PythonProject/nonebot-plugin-ocgbot-v2/nonebot_plugin_ocgbot_v2\static\decks/"
deck_json = "F:/CodeProject/PythonProject/nonebot-plugin-ocgbot-v2/nonebot_plugin_ocgbot_v2\static\decks\deck_list.json"

async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                await asyncio.sleep(3)


async def saveImg(wj_path: str, img: bytes):
    with open(wj_path, "wb") as f:  # 文件写入
        f.write(img)


async def deckDownload():
    deck_json = deck_path + "deck_list.json"
    if not os.path.exists(deck_json):
        return
    with open(deck_json, 'r', encoding='utf-8') as f:
        js = json.loads(f.read())
    for deck in js['list']:
        wjs_path = deck_path + deck
        if not os.path.exists(wjs_path):
            os.mkdir(wjs_path)
        for wj in js['list'][deck]:
            wj_path = wjs_path + "/" + wj
            if not os.path.exists(wj_path):
                saveImg(download_url(wj_path, deck_url + "{0}/{1}".format(deck, wj)))

