from pyrogram import Client
import pymongo, os
MONGO_DB = 'mongodb+srv://dinuth:dinuth@javfindxbot.ruxzq.mongodb.net/'

# with open("jsonresults.json", "w") as data:
#     json.dump(results, data, indent = 2)

dbclient = pymongo.MongoClient(MONGO_DB)
# 5224308027:AAECPvSleniPSrpKfZ-0-EmmuWlV0ZJe6dI
AUTH_USER = 1948924702
if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    bot = Client(
        "bot",
        bot_token='5224308027:AAECPvSleniPSrpKfZ-0-EmmuWlV0ZJe6dI',
        api_id=7122114,
        api_hash="3ff382cb976bdf8aead9359f2c352ac1",
        plugins=plugins
    )
    if not os.path.isdir('downloads'):  
        os.makedirs('downloads')

    #connect to the databace
    print("ready to go")
    bot.run()
