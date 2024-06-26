from asyncio import Event
from asyncio import sleep as asleep
from datetime import datetime, timedelta
from random import choice
from time import time

from pyrogram.errors.pyromod.listener_timeout import ListenerTimeout
from pyrogram.filters import command, photo, private, regex
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from SubsManager import BOT_START, Config, bot, bot_cache, bot_chats
from SubsManager.core.bot_utils import change_font, convertTime
from SubsManager.core.db_hndlr import db
from SubsManager.core.tg_utils import editMessage, sendMessage


@bot.on_message(command("start") & private)
async def start_msg(_, message):
    await sendMessage(
        message,
        f"""<b><i>Subscription Bot!</i></b>
    
    <b>• SubBot Uptime:</b> {convertTime(time() - BOT_START)}
    <b>• SubBot Version:</b> V1.2.0
    <b>• 𝗛𝗲𝗹𝗽:</b> @vipinsidersbot
    
<i>A Smart & Efficient User Subscription Management Bot, with Multiple Features to feel ease both to customers & administrators...</i>""",
        f"""<b><i>WAIT FOR A SECONDS TO LOAD PREMIUM CHANNELS!</i></b>
        
        photo="https://telegra.ph/file/c965ee91ab25f30e1879e.jpg",
        buttons=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Premium Channels Showcase", callback_data="cbbot chats"
                    )
                ],
                [
                    InlineKeyboardButton("My Plans", callback_data="cbbot myplan"),
                    InlineKeyboardButton("My Cart", callback_data="cbbot mycart"),
                    InlineKeyboardButton("Refer Others", callback_data="cbbot ref"),
                ],
                [InlineKeyboardButton("Close", callback_data="cbbot close")],
            ]
        ),
    )
    uid = message.from_user.id
    if len(message.command) > 1 and message.command[1].startswith("ref"):
        ref_user = int(message.command[1].replace("ref", "").strip())
        if uid != ref_user and uid not in (ref_eusers := await db._getUser(ref_user, "refers", {})) and not ref_eusers["is_ref"]:
            ref_eusers["uids"].append(uid)
            await db._setUserData(ref_user, key="refers", value=ref_eusers)
    await db._getUser(uid)


async def get_cinfo(cid, plan):
    c_info = await bot.get_chat(cid)
    p_info = "\n        ‣".join(
        f"Rs. {p} for {t}" for t, p in bot_chats[cid]["prices"].items()
    )
    args = "\n    • ".join(
        f"<b>{title}:</b> <i>{data}</i>"
        for title, data in bot_chats[cid]["args"].items()
    )
    return f"""<b><i>Premium Channel Details!</i></b>
    
      <b>Name:</b> {c_info.title}
    {args}
    <b>Your Selected Plan:</b> {plan}
    <b>Price List:</b>
        ‣{p_info}"""


@bot.on_callback_query(regex(r"^cbbot"))
async def global_bot_cb(client, query):
    data = query.data.split()
    message = query.message
    if data[1] == "chats":
        await query.answer()
        chats = []
        for ind, chat in enumerate(bot_chats.keys(), start=1):
            c_info = await client.get_chat(chat)
            chats.append(
                [
                    InlineKeyboardButton(
                        f"{ind}. {change_font(c_info.title)}",
                        callback_data=f"cbbot cinfo {chat}",
                    )
                ]
            )
        chats.append(
            [
                InlineKeyboardButton("<< Back", callback_data="cbbot home"),
                InlineKeyboardButton("Close", callback_data="cbbot close"),
            ]
        )
        await editMessage(message, "")
        await asleep(0.3)
        await editMessage(
            message,
            f"<b><i>Premium Channels are as Follows..:</i></b>\n\n<b>• Total Channels :</b> {len(bot_chats)}",
            buttons=InlineKeyboardMarkup(chats),
        )
    elif data[1] == "cinfo":
        await query.answer()
        pn = data[3] if len(data) > 3 else next(iter(bot_chats[int(data[2])]["prices"]))
        btns = [
            [
                InlineKeyboardButton(
                    "Show Screenshots", callback_data=f"cbbot css {data[2]}"
                ),
                InlineKeyboardButton(
                    "Change Plan", callback_data=f"cbbot splan {data[2]}"
                ),
            ],
            [
                InlineKeyboardButton("My Cart", callback_data="cbbot mycart"),
                InlineKeyboardButton(
                    "Add to Cart", callback_data=f"cbbot addcart {data[2]} {pn}"
                ),
            ],
            [
                InlineKeyboardButton("<< Back", callback_data="cbbot chats"),
                InlineKeyboardButton("Close", callback_data="cbbot close"),
            ],
        ]
        txt = await get_cinfo(int(data[2]), pn)
        await editMessage(message, "")
        await asleep(0.3)
        await editMessage(message, txt, buttons=InlineKeyboardMarkup(btns))
    elif data[1] == "css":
        await query.answer()
        await message.reply_media_group(
            [
                InputMediaPhoto(media=t_link)
                for t_link in bot_chats[int(data[2])]["sshots"]
            ]
        )
    elif data[1] == "splan":
        await query.answer()
        btns = []
        uid, cid = query.from_user.id, int(data[2])
        pz = bot_chats[cid]["prices"]
        selected = data[3] if len(data) > 3 else next(iter(pz))
        for val in pz.keys():
            if len(btns) != 0 and len(btns[-1]) < 2:
                btns[-1].append(
                    InlineKeyboardButton(
                        f"• {val} •" if val == selected else val,
                        callback_data=f"cbbot splan {cid} {val}",
                    )
                )
            else:
                btns.append(
                    [
                        InlineKeyboardButton(
                            f"• {val} •" if val == selected else val,
                            callback_data=f"cbbot splan {cid} {val}",
                        )
                    ]
                )
        btns.append(
            [
                InlineKeyboardButton(
                    "<< Back", callback_data=f"cbbot cinfo {cid} {selected}"
                ),
                InlineKeyboardButton("Close", callback_data="cbbot close"),
            ]
        )
        txt = await get_cinfo(int(data[2]), plan=selected)
        await editMessage(message, txt, InlineKeyboardMarkup(btns))
    elif data[1] == "addcart":
        uid, cid = query.from_user.id, int(data[2])
        my_cart = await db._getUser(uid, "my_cart", {})
        my_cart[str(data[2])] = {
            "expiry": None,
            "days": data[3],
            "prize": bot_chats[cid]["prices"][data[3]],
        }
        await query.answer("+ Added to Cart !", show_alert=True)
        await db._setUserData(uid, key="my_cart", value=my_cart)
    elif data[1] == "mycart":
        uid = query.from_user.id
        my_cart = await db._getUser(uid, "my_cart", {})
        if len(data) > 2 and data[2] == "empty":
            if my_cart:
                await query.answer("Emptied Cart !", show_alert=True)
                await db._setUserData(uid, key="my_cart", value={})
                my_cart = {}
            else:
                return await query.answer("Already Cart is Empty !", show_alert=True)
        else:
            await query.answer()
        total_prize = 0
        txt = "<b><i>My Cart :</i></b>\n\n"
        for no, (chat, cdata) in enumerate(my_cart.items(), start=1):
            txt += f"{no}. {(await client.get_chat(int(chat))).title}\n    • <b>Days:</b> {cdata['days']}\n    • <b>Prize:</b> Rs. {cdata['prize']}\n\n"
            total_prize += cdata["prize"]
        txt += f"• <b>Total Estimated Prize:</b> Rs. {total_prize}"
        btns = [
            [
                InlineKeyboardButton(
                    "Proceed to Buy Now !", callback_data=f"cbbot payconf {total_prize}"
                ),
                InlineKeyboardButton("Empty Cart", callback_data="cbbot mycart empty"),
            ],
            [
                InlineKeyboardButton("<< Back", callback_data="cbbot home"),
                InlineKeyboardButton("Close", callback_data="cbbot close"),
            ],
        ]
        await editMessage(message, "")
        await asleep(0.3)
        await editMessage(
            message,
            txt,
            photo="https://te.legra.ph/file/949cba8c7936a0aef636e.jpg",
            buttons=InlineKeyboardMarkup(btns),
        )
    elif data[1] == "payconf":
        uid = query.from_user.id
        if len(await db._getUser(uid, "my_cart", {})) == 0:
            return await query.answer("+ Add Some Channels to Buy", show_alert=True)
        if len(data) == 4:
            await client.stop_listening(chat_id=message.from_user.id)
        await query.answer()
        btns = [
            [
                InlineKeyboardButton(
                    "Click Here to Pay !",
                    url=f"https://pavan844.github.io/linkpe/?pa=pavan844@fam&pn=pavan&cu=INR&am={data[2]}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Confirm! Send Pay Screenshot!",
                    callback_data=f"cbbot pay {data[2]}",
                )
            ],
            [
                InlineKeyboardButton("<< Back", callback_data="cbbot mycart"),
                InlineKeyboardButton("Close", callback_data="cbbot close"),
            ],
        ]
        await editMessage(message, "")
        await asleep(0.3)
        await editMessage(
            message,
            f"• <b>Final Payment Confirm:</b>\n\nMake sure you want to Buy these Channels, then Send payment to this below button!\n\n• <b>Total Estimated Prize:</b> Rs. {data[2]}",
            photo="https://te.legra.ph/file/3692306b92aea737c4d14.jpg",
            buttons=InlineKeyboardMarkup(btns),
        )
    elif data[1] == "pay":
        await query.answer()
        btns = [
            [
                InlineKeyboardButton(
                    "Cancel Send!", callback_data=f"cbbot payconf {data[2]} cancel"
                )
            ],
            [
                InlineKeyboardButton(
                    "<< Back", callback_data=f"cbbot payconf {data[2]} can"
                ),
                InlineKeyboardButton("Close", callback_data="cbbot close"),
            ],
        ]
        await editMessage(message, "")
        await asleep(0.3)
        await editMessage(
            message,
            f"{message.caption}\n\n<b>Send me the Payment Screenshot Now! TimeOut: 60s</b>",
            buttons=InlineKeyboardMarkup(btns),
        )
        try:
            pay_ss = await message.chat.listen(filters=photo)
        except ListenerTimeout:
            await editMessage(message.caption, buttons=message.reply_markup)
            return
        else:
            await pay_ss.delete()
        ucart = await db._getUser(pay_ss.from_user.id, "my_cart", {})
        uinfo = f"""<b><i>User Details: </i></b>
        
    <b>• Name:</b> {pay_ss.from_user.mention}
    <b>• Username:</b> {pay_ss.from_user.username}
    <b>• UsedID:</b> {pay_ss.from_user.id}
    
    <b>• Payment Amount:</b> Rs. {data[2]}
    <b>• User Channels:</b> {", ".join([str((await client.get_chat(int(cid))).title) for cid in ucart.keys()])}
        """
        await sendMessage(
            Config.LOG_CHAT,
            text=uinfo,
            photo=pay_ss.photo.file_id,
            buttons=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Approve User", callback_data=f"cbbot uappr {message.id}"),
                        #InlineKeyboardButton("Ban User", callback_data=f"cbbot uban {pay_ss.from_user.id}")
                    ]
                ]
            ),
        )
        await editMessage(message, "")
        await asleep(0.3)
        if not Config.AUTO_APPROVE:
            await editMessage(
                message, f"{message.caption}\n\n<i>Wait for Admin's Approval</i>"
            )
            bot_cache[message.id] = Event()
            await bot_cache[message.id].wait()
            await sendMessage(message, "♻️ <b><i>Payment is Successfully Approved By Admin!</i></b>")
        await editMessage(
            message, f"{message.caption}\n\n<i>Generating Channels Links...</i>"
        )
        await asleep(3)

        txt = "• <u><b>Purchased Following Premium Channel(s):</b></u>\n\n"
        uid = query.from_user.id
        udata = await db._getUser(uid)
        ucart = udata.get("my_cart", {})
        prem_chats = udata.get("prem_chats", {})
        prev_trans = udata.get("prev_trans", [])

        for no, (ch, cdata) in enumerate(ucart.items(), start=1):
            cid = int(ch)
            txt += f"<b>{no}. Channel Name: {(await client.get_chat(cid)).title}</b>\n"
            txt += f"    <b>Invite Link:</b> <i>{(await client.create_chat_invite_link(cid, expire_date=datetime.now()+timedelta(days=1), member_limit=1)).invite_link}</i>\n"
            txt += f"    <b>Prem Duration:</b> <i>{cdata['days']} days</i>\n\n"
            prem_chats.update(
                {
                    ch: {
                        "expiry": datetime.now()
                        + timedelta(days=int(cdata["days"].rstrip("d"))),
                        "days": cdata["days"],
                        "prize": cdata["prize"],
                    }
                }
            )
        txt += "<b>NOTE</b>: <code>Invite Link is Only for 1 time Use and it will be expired once used by you or within 24 hrs of generation )</code>\n"

        await db._setUserData(uid, key="prem_chats", value=prem_chats)
        await db._setUserData(uid, key="my_cart", value={})
        prev_trans.append(
            {
                "prev_chats": prem_chats,
                "total_prize": int(data[2]),
                "date": datetime.today(),
            }
        )
        await db._setUserData(uid, key="prev_trans", value=prev_trans)

        await editMessage(
            message,
            txt,
            buttons=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Close", callback_data="cbbot close")]]
            ),
        )
    elif data[1] == "uappr":
        if int(data[2]) in bot_cache:
            bot_cache[int(data[2])].set()
            await query.answer("User is Approved!!", show_alert=True)
            del bot_cache[int(data[2])]
        else:
            await query.answer("User already Approved or Invalid!!", show_alert=True)
    elif data[1] == "myplan":
        await query.answer()
        uid = query.from_user.id
        udata = await db._getUser(uid, "prem_chats", {})
        txt = f"<b><i>My Plan Details:</i></b>\n\n    • <b>User :</b> {query.from_user.mention} ( #ID{query.from_user.id} )\n\n"
        if udata:
            txt += "<b><i>My Premium Channels:</i></b>\n\n"
            for no, (chat, cdata) in enumerate(udata.items(), start=1):
                txt += f"{no}. {(await client.get_chat(int(chat))).title}\n    • <b>Days:</b> {cdata['days']} | <b>Prize:</b> Rs. {cdata['prize']}\n    • <b>Premium Left:</b> {convertTime((cdata['expiry'] - datetime.now()).total_seconds())}\n\n"
        else:
            txt += "<i>Currently No Premium found for your Account..!!</i>"
        later = [
            InlineKeyboardButton(
                    "Previous Transactions", callback_data="cbbot ptrans"
                )
        ],
        btns = [
            [
                InlineKeyboardButton("<< Back", callback_data="cbbot home"),
                InlineKeyboardButton("Close", callback_data="cbbot close"),
            ],
        ]
        await editMessage(message, "")
        await asleep(0.3)
        await editMessage(message, txt, buttons=InlineKeyboardMarkup(btns))
    elif data[1] == "ref":
        await query.answer()
        uid = query.from_user.id
        ref_info = await db._getUser(uid, "refers", {})
        txt = f"• <b>My Referral Link:</b>\n\n• <b>Link :</b> https://t.me/{client.me.username}?start=ref{uid}\n• <b>Total Refers:</b> {len(ref_info['uids'])}\n\n• <b>My Referers:</b>\n\n"
        if not ref_info["uids"]:
            txt += "<i>No Referers yet..!!</i>"
        for ind, ref_user in enumerate(ref_info["uids"], start=1):
            txt += f"{ind}. {(await client.get_users(ref_user)).mention}\n"
        btns = [
            [
                InlineKeyboardButton(
                    "Share/Refer to Others >>",
                    url=f"https://telegram.me/share/url?url=https://t.me/{client.me.username}?start=ref{uid}",
                ),
                InlineKeyboardButton("Claim Benefits", callback_data="cbbot refclaim"),
            ],
            [
                InlineKeyboardButton("<< Back", callback_data="cbbot home"),
                InlineKeyboardButton("Close", callback_data="cbbot close"),
            ],
        ]
        await editMessage(message, "")
        await asleep(0.3)
        await editMessage(message, txt, buttons=InlineKeyboardMarkup(btns))
    elif data[1] == "refclaim":
        uid = query.from_user.id
        ref_info = await db._getUser(uid, "refers", {})
        if ref_info["is_ref"]:
            return await query.answer(
                f"You have already claimed your free refer bonus.. !!", 
                show_alert=True
            )
        elif len(ref_info["uids"]) < Config.REF_NEEDED:
            await query.answer(
                f"Not yet..! You still need {Config.REF_NEEDED - len(ref_info['uids'])} more refers to claim free subscription",
                show_alert=True
            )
            return
        
        prem_chats = await db._getUser(uid, "prem_chats", {})
        avl_prems = [cid for cid in bot_chats.keys() if str(cid) not in prem_chats.keys()]
        if len(avl_prems) == 0:
            return await query.answer(
                f"You already have subscription for all Premium Channels, Come later to claim free subscription when some expired..!!",
                show_alert=True
            )
        cid = choice(avl_prems)
        
        prem_chats.update(
                {
                    str(cid): {
                        "expiry": datetime.now()
                        + timedelta(days=30),
                        "days": "30d",
                        "prize": 0,
                    }
                }
        )
        await db._setUserData(uid, key="prem_chats", value=prem_chats)
        ref_info["is_ref"] = True
        await db._setUserData(uid, key="refers", value=ref_info)
        await query.answer("Claimed Benefit! Got 30d of Premium", show_alert=True)
        
        await asleep(0.6)
        
        txt = "• <u><b>Free Premium Channel:</b></u>\n\n"
        txt += f">> <b>Channel Name: {(await client.get_chat(cid)).title}</b>\n"
        txt += f"    <b>Invite Link:</b> <i>{(await client.create_chat_invite_link(cid, expire_date=datetime.now()+timedelta(days=1), member_limit=1)).invite_link}</i>\n"
        txt += f"    <b>Prem Duration:</b> <i>30 days</i>\n\n"
            
        await editMessage(message, txt, buttons=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Close", callback_data="cbbot close")]]
        ),)
    elif data[1] == "home":
        await query.answer()
        await editMessage(message, "")
        await asleep(0.3)
        await editMessage(
            message,
            f"""<b><i>Subscription Bot!</i></b>
    
    <b>• SubBot Uptime:</b> {convertTime(time() - BOT_START)}
    <b>• SubBot Version:</b> V1.2.0
    
<i>A Smart & Efficient User Subscription Management Bot, with Multiple Features to feel ease both to customers & administrators...</i>""",
            buttons=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Premium Channels Showcase", callback_data="cbbot chats"
                        )
                    ],
                    [
                        InlineKeyboardButton("My Plans", callback_data="cbbot myplan"),
                        InlineKeyboardButton("My Cart", callback_data="cbbot mycart"),
                        InlineKeyboardButton("Refer Others", callback_data="cbbot ref"),
                    ],
                    [InlineKeyboardButton("Close", callback_data="cbbot close")],
                ]
            ),
        )
    else:
        await message.delete()
        if reply_to := message.reply_to_message:
            await reply_to.delete()
