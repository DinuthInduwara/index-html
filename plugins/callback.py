import pyrogram, logging
logger = logging.getLogger(__name__)
from plugins.worker import parserAndDetails, sent_contentToTelegram, get_allPlayers, send_players, save_OnMongoDB, sendFrom_Fileid, send_players_2

@pyrogram.Client.on_callback_query()
async def cb_data(bot ,update):
    if "ne_" in update.data:
        url = update.data.split('_')[1]
        url = 'https://javfindx.com/search/video/{}'.format(url)
        results, nextpageurl = parserAndDetails(url)
        await sent_contentToTelegram(bot, update.message, results, nextpageurl)
    if "gethost_te" in update.data:
        message = update.message.caption.split('"')[1].strip()
        code = update.data.split('_')[2]
        link = "https://javfindx.com//{}/{}/".format(code, message)
        player_list = get_allPlayers(link)
        await send_players(bot, update.message, player_list, code)
    if "gethost_tosaved" in update.data:
        message = update.message.caption.split('"')[1].strip()
        code = update.data.split('_')[2]
        link = "https://javfindx.com//{}/{}/".format(code, message)
        player_list = get_allPlayers(link)
        await send_players_2(bot, update.message, player_list, code)
    if 'savein_' in update.data:
        code = update.data.split('_')[-1]
        await save_OnMongoDB(bot, update.message, code)
    if 'sendto_' in update.data:
        file_id = update.data.split('_')[1]
        await sendFrom_Fileid(bot, update.message, int(file_id))

        