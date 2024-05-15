from asyncio import sleep
from traceback import format_exc

from pyrogram.errors import (
    FloodWait,
    MessageEmpty,
    MessageNotModified,
    ReplyMarkupInvalid,
)
from pyrogram.types import InputMediaPhoto

from SubsManager import LOGGER, bot


async def sendMessage(chat, text, buttons=None, photo=None, get_error=False, **kwargs):
    try:
        if isinstance(chat, int):
            if photo:
                return await bot.send_photo(
                    chat_id=chat,
                    photo=photo,
                    caption=text,
                    reply_markup=buttons,
                    **kwargs,
                )
            return await bot.send_message(
                chat_id=chat,
                text=text,
                disable_web_page_preview=True,
                reply_markup=buttons,
                **kwargs,
            )
        else:
            if photo:
                return await bot.send_photo(
                    chat_id=chat.chat.id,
                    photo=photo,
                    caption=text,
                    reply_to_message_id=chat.id,
                    reply_markup=buttons,
                    protect_content=True,
                    **kwargs,
                )
            return await chat.reply(
                text=text,
                quote=True,
                disable_web_page_preview=True,
                reply_markup=buttons,
                **kwargs,
            )
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await sendMessage(chat, text, buttons)
    except ReplyMarkupInvalid:
        return await sendMessage(chat, text, None)
    except Exception as e:
        LOGGER.error(format_exc())
        if get_error:
            raise e
        return str(e)


async def editMessage(
    message, text, buttons=None, photo=None, get_error=False, **kwargs
):
    try:
        if message.media:
            if photo:
                return await message.edit_media(
                    media=InputMediaPhoto(media=photo, caption=text),
                    reply_markup=buttons,
                    **kwargs,
                )
            else:
                return await message.edit_caption(caption=text, reply_markup=buttons)
        return await message.edit(text=text, reply_markup=buttons, **kwargs)
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await editMessage(message, text, buttons, photo)
    except (MessageNotModified, MessageEmpty):
        pass
    except ReplyMarkupInvalid:
        return await editMessage(message, text, None, photo)
    except Exception as e:
        LOGGER.error(format_exc())
        if get_error:
            raise e
        return str(e)
