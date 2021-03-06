import logging
logger = logging.getLogger(__name__)
import pyrogram, json
from plugins.worker import javfindx_urlgen, parserAndDetails, sent_contentToTelegram, list_DB, save_forDraft, sendDraft_fromDB, delete_byID
from plugins.proxy_download import proxyDownload
from plugins.speedtest import get_speed
from plugins.rclone_upload import rclone_Upload
from plugins.bypasslinkgen import Bypass
import concurrent.futures

@pyrogram.Client.on_message(pyrogram.filters.command(["start"]))
async def start_cmd(client, message):
    await message.reply("Hi..")
    

@pyrogram.Client.on_message(pyrogram.filters.command(["s"]))
async def search_cmd(client, message):
    if len(message.command) > 1:
        txt = ''
        for i in message.command:
            if not 's' == i:
                txt+=f" {i.strip()}"
        keyword = txt.strip()
        url = javfindx_urlgen(keyword)
        results, nextpageurl = parserAndDetails(url)
        # b = json.dumps(results)
        # link_packs = process_ResponcetoListspack(results)
        # print(link_packs)
        await sent_contentToTelegram(client, message, results, nextpageurl)
        
        

@pyrogram.Client.on_message(pyrogram.filters.command(["list"]))
async def listDB_cmd(client, message):
    await list_DB(client, message)

 
@pyrogram.Client.on_message(pyrogram.filters.command(["d"]))
async def saveDraft_cmd(client, message):
    if len(message.command) > 1:
        txt = ''
        for i in message.command:
            if not 'd' == i:
                txt+=f" {i.strip()}"
        keyword = txt.strip()
        await save_forDraft(client, message, keyword)
        
        
@pyrogram.Client.on_message(pyrogram.filters.command(["drafts"]))
async def sendDraft_cmd(client, message):
    await sendDraft_fromDB(client, message)
    
@pyrogram.Client.on_message(pyrogram.filters.command(["delete"]))
async def deleteDraft_cmd(client, message):
    if len(message.command) > 1:
        id = message.command[1]
        await delete_byID(client, message, id)
        

@pyrogram.Client.on_message(pyrogram.filters.command(["download"]))
def proxyDownload_cmd(client, message):
    bypasshost = ["antfiles", "ouo", "anonfiles", "streamtape", "uservideo", "mediafire", "zippyshare", "fembed"]
    fname = None
    if len(message.command) > 1:
        url = message.command[1]
        if "|" in message.command:
            fname = message.command[3]
        if "streamtape" in url:
            ul = Bypass()
            url = ul.bypass_streamtape(url)
        if "fem=true" in message.text:
            ul = Bypass()
            url = ul.bypass_fembed(url)  
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(proxyDownload, client, message, url, fname)
            path, m = f1.result()
            rclone_Upload(path, m)


        
@pyrogram.Client.on_message(pyrogram.filters.command(["speedtest"]))
async def speedtest_cmd(client, message):
    await get_speed(client, message)