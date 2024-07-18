from datetime import datetime, timedelta
from time import sleep

from pyrogram.filters import command, user
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from SubsManager import Config, bot, bot_chats
from SubsManager.core.db_hndlr import db
from SubsManager.core.tg_utils import sendMessage


@bot.on_message(command("addprem") & user(Config.ADMINS))
async def add_prem(client, message):
    no_invite = False
    txt = message.text
    if len(txt.split()) == 1:
        return await sendMessage(message, "<i>No Data given to process further</i>")
    try:
        if txt.endswith("-nl") or "-nl" in txt:
            no_invite = True
            txt = txt.replace("-nl", "")
        data = txt.split()
        uid = int(data[1])
        d = datetime.now() + timedelta(days=int(data[-1]))
        chats = [int(c) for c in data[2:-1]]
    except Exception as e:
        return await message.reply(str(e))

    await db._setUserData(
        uid,
        key="prem_chats",
        value={str(chats[0]): {"expiry": d, "days": f"{data[-1]}d"}},
    )

    txt = "• <u><b>Invited to Following Premium Channel(s):</b></u>\n\n"

    if not no_invite:
        for no, ch in enumerate(chats, start=1):
            txt += f"<b>{no}. Channel Name: {(await client.get_chat(ch)).title}</b>\n"
            txt += f"    <b>Invite Link:</b> <i>{(await client.create_chat_invite_link(ch, expire_date=d, member_limit=1)).invite_link}</i>\n\n"
        txt += "<b>NOTE</b>: <code>Invite Link is Only for 1 time Use and it will expired once used)</code>\n"
    else:
        txt += "<i>Links have Been Provided to you by Admin..</i>\n\n"

    txt += f"• <b>Premium Duration:</b> <i>{data[-1]} days</i>"
    try:
        await sendMessage(uid, txt, get_error=True, protect_content=True)
        await message.reply("Successfully Send Invite Links to User", quote=True)
    except Exception as e:
        await message.reply_text(
            f"User has not Started Bot yet..\n\n <code>ERROR: {e}</code>"
        )


@bot.on_message(command("rmprem") & user(Config.ADMINS))
async def rm_prem(_, message):
    data = message.text.split()
    if len(data) == 1:
        return await sendMessage(message, "<i>No Data given to process further</i>")
    uid = int(data[1])
    if not (userData := await db._getUser(uid, "prem_chats")):
        return await sendMessage(message, f"No Premium Found for UserID : {uid}")

    for chat in list(userData.keys()):
        try:
            await bot.ban_chat_member(
                int(chat), uid, until_date=datetime.now() + timedelta(seconds=120)
            )
        except Exception as e:
            await sendMessage(message, str(e))
            continue
    try:
        await sendMessage(
            uid,
            "<b><i>Premium has Expired, You have been Restricted from Channel(s) !</i></b>",
            get_error=True,
        )
        await db._rmUserData(uid)
        await sendMessage(
            message, "<i>Successfully Removed from Channel & Database</i>"
        )
    except Exception as e:
        await sendMessage(
            message,
            f"User has not Started Bot yet or Maybe Blocked..\n\n <code>ERROR: {e}</code>",
        )


@bot.on_message(command("premusers") & user(Config.ADMINS))
async def all_prem(_, message):
    await message.reply(f"<b>Total Users: {await db._totalUsers()}</b>")


@bot.on_message(command("ban") & user(Config.ADMINS))
async def ban_user(_, message):
    data = message.text.split()
    if len(data) == 1:
        return await sendMessage(message, "<i>No Data given to process further</i>")
    uid = int(data[1])
    chats = [int(c) for c in data[2:]]
    waitmsg = await sendMessage(message, "<i>• Banning User ...</i>")

    txt = f"<b>User ID:</b> {uid}\n\n"
    for chat in chats:
        try:
            await bot.ban_chat_member(
                chat, uid, until_date=datetime.now() + timedelta(seconds=60)
            )
            txt += f"<i>Banned from </i><code>{chat}</code>\n"
        except Exception as err:
            txt += f"<code>{chat}: {err}</code>"
            continue

    await waitmsg.delete()
    await sendMessage(message, txt)


@bot.on_message(command(["broadcast", "bc", "grp_bc", "grp_broadcast"]) & user(Config.ADMINS))
async def broadcast(_, message):
    is_grpbc = bool(message.command[0] in ["grp_bc", "grp_broadcast"])

    if not message.reply_to_message:
        return await message.reply(f"<code>Use this command as a reply to any telegram message to broadcast to all {"groups" if is_grpbc else "users"}.</code>")
        
    query = await db._getAllGrps() if is_grpbc else await db._getAllUsers()
    broadcast_msg = message.reply_to_message
    total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0
    pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
    async for row in query:
        chat_id = row["_id"]
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            sleep(e.value * 1.1)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await db._rmGroup(chat_id) if is_grpbc else await db._rmUserData(chat_id)
            blocked += 1
        except InputUserDeactivated:
            await db._rmGroup(chat_id) if is_grpbc else await db._rmUserData(chat_id)
            deleted += 1
        except Exception as e:
            LOGGER.error(str(e))
            unsuccessful += 1
        total += 1

    status = f"""📡 <b><u>Broadcast Completed</u></b>

🗄 Total {"Groups" if is_grpbc else "Users"}: <code>{total}</code>
📈 Successful: <code>{successful}</code>
🔐 Blocked {"Groups" if is_grpbc else "Users"}: <code>{blocked}</code>
📮 Deleted Chats: <code>{deleted}</code>
📉 Unsuccessful: <code>{unsuccessful}</code>"""
    await pls_wait.edit(status)
    
    
@bot.on_message(command("channels") & user(Config.ADMINS))
async def get_channels(client, message):
    txt = "<b> All Channels </b>\n\n"
    txt += "\n".join([(await client.get_chat(cid)).title for cid in bot_chats.keys()])
    await sendMessage(message, txt)
    