import requests, json, os, time
from pyrogram import Client, filters
from pySmartDL import SmartDL
from plugins.tg_upload import upload_tg, humanbytes
from plugins.rclone_upload import rclone_Upload
proxy = []
@Client.on_message(filters.document)
async def setproxy_cmd(client, message):
    print(message)
    if message.document.mime_type == "application/json": 
        doc =await message.download()
        with open(doc, 'r') as f:
            print("proxy appended from document")
            proxy.append(json.load(f))
            os.remove(doc)


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
}
def proxyDownload(client, message, url, filename=None):
    session = requests.Session()
    response = session.get(url, stream=True)
    try:
        mtype = response.headers.get('content-type').split('/')[-1]
        fname = url.split('/')[-1]+'.'+mtype
        try:
            n = url.split('/')[-1].split('.')[-1]
            if len(n.split()) < 5:
                fname = url.split('/')[-1]
        except: pass
        if filename is not None:
            fname = filename
        if len(fname) > 20:
            fname = 'opencode devs.{}'.format(mtype)
        print(fname)
        path = './downloads/{}'.format(fname)
        
        
        size = humanbytes(int(response.headers.get('content-length', 0)))
        obj = SmartDL(url,'./downloads/{}'.format(path), progress_bar=False, timeout=15)
        obj.start(blocking=False)
        
        msg = "File Is Downloading..!"
        m = message.reply(msg)
        while not obj.isFinished():
            try:
                ms = "File Is Downloading..!\n🚴‍♂️ **Done:** `{}`\n🎚️ **Total:** `{}`\n🏍️ **Speed:** `{}/`\n⏱️ **ETA:** `{}`\n⏳ **Percentage:** `{}%`\n\n{}".format(obj.get_dl_size(human=True), size, obj.get_speed(human=True), obj.get_eta(human=True), int((obj.get_progress()*100)), obj.get_progress_bar())
                m.edit(ms)
                time.sleep(3)
            except Exception as e:
                print(e)
                pass
        if obj.isSuccessful():
                path = obj.get_dest()
                # d_time =  obj.get_dl_time(human=True)
                # upload_tg(client, message, path, m)
                rclone_Upload(path, m)
        else:
            msg = ''
            for e in obj.get_errors():
                msg+=str(e)
            m.edit("There were some errors:")

        return path
    except Exception as error:
        message.reply(error)
        return None
    