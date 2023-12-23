from os import environ
import logging
import telebot
from kesha import compressor
from kesha.kesha import const

bot = telebot.TeleBot(environ.get("BOT_TOKEN"))


def download(file):
    """Download file"""
    file = bot.get_file(file)
    logging.debug(file.file_path)
    content = bot.download_file(file.file_path)
    with open(file.file_path, "wb") as downloaded:
        downloaded.write(content)
    return file


def image_compress(msg):
    bot.send_chat_action(msg.chat.id, "upload_photo", 5)
    file = download(msg.reply_to_message.photo[0].file_id)
    with open(file.file_path, "rb") as photo:
        bot.send_photo(msg.chat.id, photo, reply_to_message_id=msg.message_id)


def unified_compress(msg, target, compress, send):
    bot.send_chat_action(msg.chat.id, "upload_document", 5)
    if target.duration < const.MAX_VIDEO_AND_AUDIO_LENGTH:
        file = download(target.file_id)
        try:
            result = compress(file.file_path)
        except compressor.exceptions.NonZeroExitCodeReturned:
            bot.reply_to(msg, const.ERRS["fail"])
        else:
            with open(result, "rb") as baked:
                send(msg.chat.id, baked, reply_to_message_id=msg.message_id)
    else:
        bot.reply_to(msg, const.ERRS["too_long"])
        logging.info(f"File is too long ({target.duration}s)")


@bot.message_handler(commands=["c"])
def compress_cmd(msg):
    if msg.reply_to_message.video:
        unified_compress(msg, msg.reply_to_message.video, compressor.compress_video, bot.send_video)
    elif msg.reply_to_message.voice:
        unified_compress(msg, msg.reply_to_message.voice, compressor.compress_audio, bot.send_voice)
    elif msg.reply_to_message.video_note:
        unified_compress(msg, msg.reply_to_message.video_note, compressor.compress_video,
                         bot.send_video_note)
    elif msg.reply_to_message.audio:
        unified_compress(msg, msg.reply_to_message.audio, compressor.compress_audio, bot.send_audio)
    elif msg.reply_to_message.photo:
        image_compress(msg)
    else:
        bot.reply_to(msg, const.ERRS["no_file"])


@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, const.START)


def main():
    bot.infinity_polling()
