import pyrogram, mimetypes, time, math, os
from typing import Union
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import FloodWait



PROGRESS = """
🚴‍♂️ **Done:** `{0}`
🎚️ **Total:** `{1}`
🏍️ **Speed:** `{2}/s`
⏱️ **ETA:** `{3}`
⏳ **Percentage:** `{4}%`
"""
# def progress_for_pyrogram(
#     current,
#     total,
#     ud_type,
#     message,
#     start
# ):
#     now = time.time()
#     diff = now - start
#     if round(diff % 10.00) == 0 or current == total:
#         # if round(current / total * 100, 0) % 5 == 0:
#         percentage = current * 100 / total
#         speed = current / diff
#         elapsed_time = round(diff) * 1000
#         time_to_completion = round((total - current) / speed) * 1000
#         estimated_total_time = elapsed_time + time_to_completion

#         elapsed_time = TimeFormatter(milliseconds=elapsed_time)
#         estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

#         progress = "[{0}{1}] \nP: {2}%\n".format(
#             ''.join(["█" for i in range(math.floor(percentage / 5))]),
#             ''.join(["░" for i in range(20 - math.floor(percentage / 5))]))

#         tmp = progress + PROGRESS.format(
#             humanbytes(current),
#             humanbytes(total),
#             humanbytes(speed),
#             # elapsed_time if elapsed_time != '' else "0 s",
#             estimated_total_time if estimated_total_time != '' else "0 s",
#             round(percentage, 2)
#         )
#         try:
#             await message.edit(
#                 text="{}\n {}".format(
#                     ud_type,
#                     tmp
#                 )
#             )
#         except:
#             pass



async def progress_for_pyrogram(
    current,
    total,
    message
):
    start = time.perf_counter()
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="{}".format(
                    tmp
                )
            )
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'
def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " days, ") if days else "") + \
          ((str(hours) + " hours, ") if hours else "") + \
          ((str(minutes) + " min, ") if minutes else "") + \
          ((str(seconds) + " sec, ") if seconds else "") + \
          ((str(milliseconds) + " millisec, ") if milliseconds else "")
    return tmp[:-2]
def get_type(path):
    kind = mimetypes.guess_type(path)
    if 'image' in kind[0]:
        return "photo"
    elif "audio" in kind[0]:
        return "audio"
    elif "video" in kind[0]:
        return "video"
    else:
        return "document"

async def progress_for_pyrogram(current, total):
    await msg.edit(f"{current / total}")


    
def upload_tg(client, message, path, m):
    global msg
    msg = m
    tg_upload_type = get_type(path)
    if tg_upload_type == "photo":
        client.send_photo(message.chat.id, photo=path, caption=os.path.basename(path), progress=progress_for_pyrogram)
        os.remove(path)
    elif tg_upload_type == "audio":
        client.send_audio(message.chat.id, audio=path, title=os.path.basename(path), progress=progress_for_pyrogram)
        os.remove(path)
    elif tg_upload_type == "video":
        client.send_video(message.chat.id, video=path, file_name=os.path.basename(path), progress=progress_for_pyrogram)
        os.remove(path)
    elif tg_upload_type == "document":
        client.send_document(message.chat.id, document=path, file_name=os.path.basename(path), progress=progress_for_pyrogram)
        os.remove(path)