import logging
logger = logging.getLogger(__name__)
import pyrogram, json
from plugins.worker import javfindx_urlgen, parserAndDetails, sent_contentToTelegram, list_DB, save_forDraft, sendDraft_fromDB, delete_byID
from plugins.proxy_download import proxyDownload
from plugins.speedtest import get_speed
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
    fname = None
    if len(message.command) > 1:
        url = message.command[1]
        if "|" in message.command:
            fname = message.command[3]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(proxyDownload, client, message, url, fname)
            path = f1.result()
            print(path)

        
@pyrogram.Client.on_message(pyrogram.filters.command(["speedtest"]))
async def speedtest_cmd(client, message):
    await get_speed(client, message)