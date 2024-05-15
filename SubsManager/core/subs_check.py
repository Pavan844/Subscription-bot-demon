from asyncio import sleep
from datetime import datetime, timedelta

from SubsManager import LOGGER, bot
from SubsManager.core.db_hndlr import db
from SubsManager.core.tg_utils import sendMessage


async def subs_check():
    while 1:
        async for row in await db._getAllUsers():
            uid = int(row["_id"])
            for chat, cdata in row["prem_chats"].items():
                exp = cdata["expiry"]
                if isinstance(exp, str):
                    exp = datetime.strptime(exp, "%Y-%m-%d %H:%M:%S.%f")
                if exp <= datetime.now():
                    try:
                        await bot.ban_chat_member(
                            int(chat),
                            uid,
                            until_date=datetime.now() + timedelta(seconds=120),
                        )
                    except Exception as e:
                        LOGGER.error(str(e))
                        continue
                    else:
                        await db._rmUserData(uid)
                        await sendMessage(
                            uid,
                            f"<b><i>Premium has Expired, You have been Restricted from Channel, {chat} !!</i></b>",
                        )
        await sleep(10800)
