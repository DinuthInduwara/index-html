from datetime import timedelta



def human_readable_bytes(value, digits=2, delim="", postfix=""):
    """Return a human-readable file size."""
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix


def human_readable_timedelta(seconds, precision=0):
    """Return a human-readable time delta as a string."""
    pieces = []
    value = timedelta(seconds=seconds)

    if value.days:
        pieces.append(f"{value.days}d")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}h")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}m")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])





from speedtest import Speedtest



async def get_speed(bot, message):
    imspd = await message.reply_text("`Running speedtest...`", quote=True)
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    (result["share"])
    string_speed = f"""
**Speedtest Result:-**
Server Name: `{result["server"]["name"]}`
Country: `{result["server"]["country"]}, {result["server"]["cc"]}`
Sponsor: `{result["server"]["sponsor"]}`
Upload: `{human_readable_bytes(result["upload"] / 8)}/s`
Download: `{human_readable_bytes(result["download"] / 8)}/s`
Ping: `{result["ping"]} ms`
ISP: `{result["client"]["isp"]}`
"""
    await imspd.edit(string_speed)
