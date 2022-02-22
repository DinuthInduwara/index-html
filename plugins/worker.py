from bs4 import BeautifulSoup
from main import AUTH_USER, dbclient
import requests, re, asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.proxy_download import proxyDownload
from bson.objectid import ObjectId
def javfindx_urlgen(keywoard=None):
    if keywoard is not None:
        if ' ' in keywoard:
            keywoard = keywoard.replace(' ', '+') 
        searchbace = f'https://javfindx.com/search/video/?s={keywoard}'
        print(searchbace)
    return searchbace


def parserAndDetails(url):
    result = {}
    nextpage = None
    r = requests.get(url)
    soup =BeautifulSoup(r.text, 'html.parser') 
    count = 0
    for i in soup.find_all('div' ,class_="well well-sm"):
        duration = i.find('span', class_='time-video badge1 transparent').text.strip()
        r_date = i.find('span', class_='pull-left').text.strip()

        contenturl = re.findall(r'/\d[^/].+/',str(i))[0]
        baceurl = f'https://javfindx.com/{contenturl}'
        poster_link = re.findall(r'https.*.jpg', str(i))[0]
        title_text = re.findall(r'title=.*"',str(i))[0]
        title =re.split(r'title="', title_text)[1]
        title =re.split(r'"',title)[0]
        vid_count = f'video{count}'
        result[vid_count] = {
            "name":title,
            "URL":baceurl,
            "Poster":poster_link,
            "duration":duration,
            "release_date": r_date
        }
        count += 1
    result['PAGEURL'] = url  
    if result is not None:
        find = soup.find_all('a', class_='prevnext')
        for i in find:
            if 'fa fa-arrow-right' in  str(i.find('i', class_='fa fa-arrow-right')):
                nextpage = i["href"].strip()
                return result, nextpage
        
    return result, nextpage


async def send_players_2(client, message, on_list, code):
    inline_keyboard= []
    for i in on_list:
        player = i.get("player")
        p_url = i.get("player_link")
        inline_keyboard.append([InlineKeyboardButton(player, url=p_url)])
    await client.edit_message_caption(message.chat.id,message.message_id, caption=message.caption,reply_markup=InlineKeyboardMarkup(inline_keyboard))



async def sent_contentToTelegram(client, message, responce, nextpageurl):
    for count, details in responce.items():
        try:
            await client.send_photo(message.chat.id,photo=details["Poster"], caption=f"""
☘️ Tιтle : "`{details["name"]}`"
                                    
🕰 𝙳𝚞𝚛𝚊𝚝𝚒𝚘𝚗 : `{details["duration"]}`
                                    
📅𝚁𝚎𝚕𝚎𝚊𝚜𝚎 : `{details["release_date"]}`
                                    """, reply_markup=InlineKeyboardMarkup([[
                                            InlineKeyboardButton("watch", callback_data="gethost_te_{}".format(details["URL"].split("/")[4]))
                        ]]))
        except:
            pass
    try:
        if nextpageurl is not None:
            await client.send_message(message.chat.id, text="More Videos", reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Next Page', callback_data='ne_{}'.format(nextpageurl.split('javfindx.com/search/video/')[1]))]]))
    except AttributeError:
        pass



def get_allPlayers(url):
    details =[]
    r = requests.get(url)
    soup =BeautifulSoup(r.text, 'html.parser')
    for i in soup.find_all('button1' ,class_="button_choice_server"):
        p_url = i["onclick"].split("'")[1]
        p = i.text
        shema = {
            "player": p,
            "player_link": p_url
        }
        details.append(shema)
    return details

async def send_players(client, message, on_list, code):
    inline_keyboard= []
    for i in on_list:
        player = i.get("player")
        p_url = i.get("player_link")
        inline_keyboard.append([InlineKeyboardButton(player, url=p_url)])
    if AUTH_USER == message.chat.id:
        inline_keyboard.append([InlineKeyboardButton('Save For Later', callback_data="savein_{}".format(code))])
    await client.edit_message_caption(message.chat.id,message.message_id, caption=message.caption,reply_markup=InlineKeyboardMarkup(inline_keyboard))


async def save_OnMongoDB(client, message, code):
    db_col =  dbclient["JavFindX"]["Saved"]
    msg = await client.get_messages(message.chat.id, message.message_id)
    msgid = msg.message_id
    shema = {
        "message_id": msgid,
        "code": code
    }
    
    x = db_col.insert_one(shema)
    await client.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("remove", callback_data="remove_{}".format(msgid))]]))
    print(x.inserted_id)


def getSavedSetsFromDB():
    db_col =  dbclient["JavFindX"]["Saved"]
    ls = [i for i in db_col.find()]
    ls_set = []
    for i in range(0, len(ls), 5):
        list_set = ls[i:i+5]
        ls_set.append(list_set)
    return ls_set


async def list_DB(client, message):
    ls_set = getSavedSetsFromDB()
    inline_keyboard = []
    for i in ls_set:
        ik = []
        for l in i:
            id = l.get("message_id")
            code = l.get("code")
            ik.append(InlineKeyboardButton(id, callback_data='sendto_{}'.format(id)))
        inline_keyboard.append(ik)
    await message.reply("select you wont", reply_markup=InlineKeyboardMarkup(inline_keyboard), quote=True)
    
async def sendFrom_Fileid(client, message, id):
    msg = await client.get_messages(message.chat.id, id)
    caption, photo = msg.caption, msg.photo.file_id
    await client.send_photo(message.chat.id,photo=photo, caption=caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("watch", callback_data="gethost_tosaved_{}".format(id))]]))

async def save_forDraft(client, message, keyword):
    db_col =  dbclient["JavFindX"]["Draft"]
    shema = {"message":keyword}
    x = db_col.insert_one(shema)
    await message.reply("{} is added to draft, its id is `{}`".format(keyword, x.inserted_id))

async def delete_byID(client, message, id):
    db_col =  dbclient["JavFindX"]["Draft"]
    x = db_col.delete_one({'_id': ObjectId(id)})
    await message.reply("`{}` is deleted!".format(id, x.deleted_count))


async def sendDraft_fromDB(client, message):
    db_col =  dbclient["JavFindX"]["Draft"]
    ls = [i for i in db_col.find()]
    mg = "You saved \n\n"
    for i in ls:
        keyword = i.get("message")
        id = i.get("_id")
        msg = "⦿  {} : `{}` \n".format(keyword, id)
        mg+=msg
    await message.reply(mg, disable_web_page_preview=True)
    
def handleDownloads(client, message, url, fname):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(proxyDownload(client, message, url, fname))
    loop.close()