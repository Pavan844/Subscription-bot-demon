from asyncio import create_subprocess_exec
from os import execl
from os import path as ospath
from sys import executable

from aiofiles import open as aiopen
from pyrogram import idle
from pyrogram.filters import command, user

from SubsManager import LOGGER, Config, bot
from SubsManager.core.subs_check import subs_check


@bot.on_message(command("restart") & user(Config.ADMINS))
async def restart_hndlr(_, message):
    restart_message = await message.reply("<i>Restarting...</i>")
    await (await create_subprocess_exec("python3", "update.py")).wait()
    async with aiopen(".restartmsg", "w") as f:
        await f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    execl(executable, executable, "-m", "SubsManager")


async def restart():
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id, text="<i>Restarted !</i>"
            )
        except Exception as e:
            LOGGER.error(e)


async def main():
    await bot.start()
    await restart()
    bot.loop.create_task(subs_check())
    LOGGER.info("Subscription Bot Started!")
    await idle()
    await bot.stop()


if __name__ == "__main__":
    bot.run(main())
