from discord.ext import commands
import discord
import os, time
from roblopy import *
import asyncio
from random import randint, choice, shuffle
import json
import sys
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
import uuid
from cryptography.fernet import Fernet
import base64
import subprocess
import ast 
import math

key = ""


obj = Fernet(key)




print("Initiating...")

bot = commands.Bot(command_prefix='!',description="Limited Sniper Bot")
bot.remove_command('help')

base = declarative_base()
engine = db.create_engine(
    f'mysql+mysqlconnector://dbPath',
    echo=False)
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

class ActiveInstances(base):
    __tablename__ = 'ActiveInstances'
    id = db.Column(db.Integer,primary_key=True)
    channelid = db.Column(db.BigInteger,nullable=False)
    xtoken = db.Column(db.String(length=40),nullable=False)
    perc = db.Column(db.Float,nullable=False)
    cookie = db.Column(db.String(length=1000),nullable=False)
    mode = db.Column(db.Integer,nullable=False)
    method = db.Column(db.String(length=40),nullable=False)
    itemids = db.Column(db.String(length=10000),nullable=False)
    numbest = db.Column(db.Integer,default=48)
    user = db.Column(db.String(length=60),nullable=False)

    def __repr__(self):
        return str(self.channelid)

class Projecteds(base):
    __tablename__ = 'Projecteds'
    id = db.Column(db.Integer,primary_key=True)
    assetid = db.Column(db.BigInteger,nullable=False)

    def __repr__(self):
        return str(self.assetid)

class CheckerWhitelist(base):
    __tablename__ = 'CheckerWhitelist'
    id = db.Column(db.Integer,primary_key=True)
    hwid = db.Column(db.String(50),nullable=False)
    name = db.Column(db.String(50),nullable=False)
    pages = db.Column(db.String(10),nullable=False)
    vpsnum = db.Column(db.Integer,nullable=False)
    listnum = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return str(self.name)

class Priorities(base):
    __tablename__ = 'Priorities'
    id = db.Column(db.Integer,primary_key=True)
    channelid = db.Column(db.BigInteger,nullable=False)

    def __repr__(self):
        return str(self.channelid)

hwid = str(uuid.UUID(int=uuid.getnode()))
#print(session.query(CheckerWhitelist).all())
if not session.query(db.exists().where(CheckerWhitelist.hwid == hwid)).scalar():
    print("Please get a whitelist! Contact on discord! Removing all files!")
    os.remove("config.ini")
    os.remove("info.ini")
    os.remove("readme.md")
    os.remove("roblopy.pyc")
    os.remove("setup.pyc")
    os.remove("updater.pyc")
    os.remove("checker.pyc")
    sys.exit()
quere = session.query(CheckerWhitelist).filter(CheckerWhitelist.hwid == hwid).first()
vpsnum = quere.vpsnum
listnum = quere.listnum

if hwid == "":
    initdb = input("Init DB? [Y/N] ")
    if initdb.lower() == "y":
        passtest = input("Please enter in the password: ")
        if passtest == "".decode("utf-8"):
            print("Init DB!!")
            base.metadata.create_all()
        else:
            print("Failed!! Restart to try again!")


loop = {}
inuse = {}
rapDict = {}
nameDict = {}
old = {}
projecteds = {}
blacklisted = []
story = True
errorcookies = []
instances = []
ProductIds = {}
#sellers = {}
yellow = 0xeee657
red = 0xff0000
green = 0x32cd32
purple = 0x6a0dad

client = RobloxApiClient()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

print("Starting Up!")
# with open("projecteds.txt", "r", encoding="utf-8") as f:
#     d = f.readlines()
#     f.seek(0)
#     for i in d:
#         blacklisted.append(int(i.strip))
# print(blacklisted)

def getErrorCookies():
    with open("config.ini", "rb") as f:
        d = f.readlines()
        f.seek(0)
        for pos, line in enumerate(d):
            try:
                line = str(obj.decrypt(line))
                line = line.replace("b'", "").replace("'", "").replace(r"\n", "") #'
            except:
                pass
            errorcookies.append(line.strip())

getErrorCookies()

if hwid == "":
    ti = str(input("Enter Pages (EX: 1-4): "))
else:
    ti = quere.pages

# async def getResellers(itemid, cookie):
#     global sellers
#     sellers[itemid] = await client.getSellers(itemid, cookie)


async def discordInstance(instance, result):
    global ProductIds
    #global sellers
    set = str(instance.mode)
    perc = instance.perc
    channelid = instance.channelid
    ctx = bot.get_channel(channelid)
    certain = instance.method
    cookie = instance.cookie
    itemids = ast.literal_eval(instance.itemids)
    numbest = instance.numbest
    token = instance.xtoken
    if set == "1":
        oldprice = result.get("OldPrice")
        price = result.get("BestPrice")
        if certain == "file":
            if str(result.get("AssetId")) in itemids:
                continueon = True
            else:
                continueon = False
        elif certain == "best":
            if int(result.get("Page")) <= int(numbest):
                continueon = True
            else:
                continueon = False
        else:
            continueon = True
        if float(perc) <= result.get(1) and continueon:
            responseb = await client.buyItem(result.get("AssetId"), cookie, price, token, ProductIds.get(result.get("AssetId")))
            print("BUY!!")
            link = result.get("AbsoluteUrl")
            link2 = f'https://www.rolimons.com/item/{result.get("AssetId")}'
            if responseb == False:
                pass
                # embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. It dropped from {oldprice} to {price}. - VPS #{str(vpsnum)}')
                # embed.add_field(name='❌', value=f'**{result.get("Name")} was already bought :(**', inline=False)
                # embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                # embed.set_footer(text='Bot made')
                # await ctx.send(embed=embed)
            elif responseb == None:
                item = session.query(ActiveInstances).filter(ActiveInstances.channelid == channelid).first()
                session.delete(item)
                session.commit()
                embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. It dropped from {oldprice} to {price}. - VPS #{str(vpsnum)}')
                embed.add_field(name='❌', value=f'**Cookie has became incorrect! The bot has stopped!**', inline=False)
                embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                embed.set_footer(text='Bot made')
                await ctx.send(embed=embed)
            elif responseb == "False2":
                pass
                # embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. It dropped from {oldprice} to {price}. - VPS #{str(vpsnum)}')
                # embed.add_field(name='❌', value=f'**Please refill my robux!! I don\'t have enough to buy this item!**', inline=False)
                # embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                # embed.set_footer(text='Bot made')
                # await ctx.send(embed=embed)
            elif responseb == "False3":
                embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. It dropped from {oldprice} to {price}. - VPS #{str(vpsnum)}')
                embed.add_field(name='❌', value=f'**You already own this item silly xD!**', inline=False)
                embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                embed.set_footer(text='Bot made')
                await ctx.send(embed=embed)
            elif responseb == True:
                embed = discord.Embed(color=green, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. It dropped from {oldprice} to {price}. - VPS #{str(vpsnum)}')
                embed.add_field(name='✅', value=f'**Bought {result.get("Name")} at {link} and {link2} for {price}**', inline=False)
                embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                embed.set_footer(text='Bot made')
                await ctx.send(embed=embed)
            else:
                if "InternalServerError" in responseb:
                    pass
                elif "Incorrect Token" == responseb:
                    pass
                else:
                    embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. It dropped from {oldprice} to {price}. - VPS #{str(vpsnum)}')
                    embed.add_field(name='❌', value=f'**Error {responseb}**', inline=False)
                    embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                    embed.set_footer(text='Bot made')
                    await ctx.send(embed=embed)
    if set == "2":
        rap = result.get("Rap")
        price = result.get("BestPrice")
        if certain == "file":
            if str(result.get("AssetId")) in itemids:
                continueon = True
            else:
                continueon = False
        elif certain == "best":
            if int(result.get("Page")) <= int(numbest):
                continueon = True
            else:
                continueon = False
        else:
            continueon = True
        if float(perc) <= result.get(2) and continueon:
            responseb = await client.buyItem(result.get("AssetId"), cookie, price, token, ProductIds.get(result.get("AssetId")))
            print("BUY!!")
            link = result.get("AbsoluteUrl")
            link2 = f'https://www.rolimons.com/item/{result.get("AssetId")}'
            if responseb == False:
                pass
                # embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. The rap was {rap} but it dropped to {price}. - VPS #{str(vpsnum)}')
                # embed.add_field(name='❌', value=f'**{result.get("Name")} was already bought :(**', inline=False)
                # embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                # embed.set_footer(text='Bot made')
                # await ctx.send(embed=embed)
            elif responseb == None:
                item = session.query(ActiveInstances).filter(ActiveInstances.channelid == channelid).first()
                session.delete(item)
                session.commit()
                embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. The rap was {rap} but it dropped to {price}. - VPS #{str(vpsnum)}')
                embed.add_field(name='❌', value=f'**Cookie has became incorrect! The bot has stopped!**', inline=False)
                embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                embed.set_footer(text='Bot made')
                await ctx.send(embed=embed)
            elif responseb == "False2":
                pass
                # embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. The rap was {rap} but it dropped to {price}. - VPS #{str(vpsnum)}')
                # embed.add_field(name='❌', value=f'**Please refill my robux!! I don\'t have enough to buy this item!**', inline=False)
                # embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                # embed.set_footer(text='Bot made')
                # await ctx.send(embed=embed)
            elif responseb == "False3":
                embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. The rap was {rap} but it dropped to {price}. - VPS #{str(vpsnum)}')
                embed.add_field(name='❌', value=f'**You already own this item silly xD!**', inline=False)
                embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                embed.set_footer(text='Bot made')
                await ctx.send(embed=embed)
            elif responseb == True:
                embed = discord.Embed(color=green, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. The rap was {rap} but it dropped to {price}. - VPS #{str(vpsnum)}')
                embed.add_field(name='✅', value=f'**Bought {result.get("Name")} at {link} and {link2} for {price}**', inline=False)
                embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                embed.set_footer(text='Bot made')
                await ctx.send(embed=embed)
            else:
                if "InternalServerError" in responseb:
                    pass
                elif "Incorrect Token" == responseb:
                    pass
                else:
                    embed = discord.Embed(color=red, title=f'Found Snipe {result.get("Name")} at {link} and {link2}. The rap was {rap} but it dropped to {price}. - VPS #{str(vpsnum)}')
                    embed.add_field(name='❌', value=f'**Error {responseb}**', inline=False)
                    embed.set_thumbnail(url=result.get("ThumbnailUrl"))
                    embed.set_footer(text='Bot made')
                    await ctx.send(embed=embed)


async def itemUpdater(i):
    print(f"Item Updater {i}")
    await asyncio.sleep(10)
    await asyncio.sleep(float(randint(1,5)) * 0.1)
    print(f"Started {i}")
    global inuse
    global old
    global rapDict
    global projecteds
    global blacklisted
    global instances
    global ProductIds
    async def setfakecookie(i):
        global errorcookies
        cookiechose = choice(errorcookies)
        if cookiechose not in inuse.values():
            if await client.testcookie(cookiechose):
                inuse[i] = cookiechose
                return cookiechose
            else:
                print("Uh oh")
                errorcookies.remove(cookiechose)
                await setfakecookie(i)
        else:
            await setfakecookie(i)
        # with open("config.ini", "rb") as f:
        #     d = f.readlines()
        #     f.seek(0)
        #     randomNum = randint(0, numLines)
        #     for pos, line in enumerate(d):
        #         try:
        #             line = str(obj.decrypt(line))
        #             line = line.replace("b'", "").replace("'", "").replace(r"\n", "") #'
        #         except:
        #             pass
        #         #print(line.strip())
        #         if pos == randomNum and line.strip() not in inuse.values():
        #             if line.strip() == "DOES NOT WORK":
        #                 await setfakecookie(i)
        #             #print(await client.testcookie(line.strip()))
        #             if await client.testcookie(line.strip()):
        #                 inuse[i] = line.strip()
        #                 return line.strip()
        #             else:
        #                 print("Uh oh", pos)
        #                 with open("config.ini", "rb") as f:
        #                     d = f.readlines()
        #                     f.seek(0)
        #                     with open("config.ini", "w") as f:
        #                         for i in d:
        #                             try:
        #                                 oldi = str(i).replace("b'", "").replace("'", "").replace(r"\n", "")
        #                                 i = str(obj.decrypt(i))
        #                                 i = i.replace("b'", "").replace("'", "").replace(r"\n", "") #'
        #                                 #print(i.strip(), line.strip())
        #                                 if i.strip() != line.strip():
        #                                     f.write(str(oldi) + "\n")
        #                                 # else:
        #                                 #     print("here")
        #                                 #     f.write("DOES NOT WORK\n")
        #                             except Exception as e:
        #                                 print(e)
        #                                 #pass
        #                         #f.truncate()
        #                 with open("config.ini", "r", encoding="utf-8") as f:
        #                     d = f.readlines()
        #                     f.seek(0)
        #                     for pos, line in enumerate(d):
        #                         numLiness = pos
        #                 numLines = numLiness
        #                 await setfakecookie(i)
    cookiefake = await setfakecookie(i)
    sort = 2
    freq = 1
    # sort = -1
    # freq = -1
    #seti = i + 47 #3
    keyword = None
    while True:
        try:
        #if True:
            #t1 = time.time()
            search = await client.catalogSearch(False,cookiefake,-1, -1, 2, 2, -1, sort, freq, keyword, 1, 0,  None, True,  i,  -1)
            if search == None:
                keepGoingN = True
                while keepGoingN:
                    cookiefake = await setfakecookie(i)
                    search = await client.catalogSearch(False,cookiefake,-1, -1, 2, 2, -1, sort, freq, keyword, 1, 0,  None, True,  i,  -1)
                    if search != None:
                        keepGoingN = False
            for result in search:
                rap = int(rapDict.get(str(result.get("AssetId"))))
                #blacklisted = json.loads(str(session.query(Projecteds).all()))
                if result.get("BestPrice") != "" and rap != None and str(result.get("AssetId")) not in str(projecteds.keys()) and result.get("AssetId") not in blacklisted:
                    price = int(result.get("BestPrice").replace(',', ''))

                    if old.get(result.get("AssetId")) != None:
                        passed = True
                    else:
                        passed = False
                    if passed:
                        #if result.get("BestPrice") < old[result.get("AssetId")] and result.get("BestPrice") < rap:
                        result["BestPrice"] = price
                        if result.get("BestPrice") < old[result.get("AssetId")]:
                            #loopr.create_task(getResellers(result.get("AssetId"), cookiefake))
                            #print("Here")
                            #result.update({"Changed": True})
                            result.update({"Rap": rap})
                            result.update({"OldPrice": old[result.get("AssetId")]})
                            perc = result.get("BestPrice") / old[result.get("AssetId")]
                            perc = round(1-perc,2)
                            perc2 = result.get("BestPrice") / rap
                            perc2 = round(1-perc2,2)
                            if perc > 0.01:
                                result.update({1: perc, 2: perc2, "Page": i})
                                for instance in instances:
                                    loopr.create_task(discordInstance(instance, result))
                                print(f"Found Snipe on page {i}, {result.get('Name')}, Price %: {perc}, Rap %: {perc2}")
                    else:
                        productresult = await client.getItemInfo(result.get("AssetId"), cookiefake)
                        if productresult == None:
                            keepGoing = True
                            while keepGoing:
                                cookiefake = await setfakecookie(i)
                                productresult = await client.getItemInfo(result.get("AssetId"), cookiefake)
                                if productresult != None:
                                    keepGoing = False
                        #print(ProductIds)
                        ProductIds[result.get("AssetId")] = productresult
                    old[result.get("AssetId")] = price
            #print(time.time() - t1)
            # if i <= seti:
            #     i = i + 1
            # else:
            #     i = i - 47 #3
        except Exception as e:
            #pass
            print(e, sys.exc_info()[-1].tb_lineno)

async def dbProjectedUpdater():
    global blacklisted
    print("Starting Blacklisted Updater")
    session = orm.scoped_session(orm.sessionmaker())(bind=engine)
    blacklisted = json.loads(str(session.query(Projecteds).all()))
    #session.close()
    print(blacklisted)
    print("Done init")
    while True:
        await asyncio.sleep(60) #60
        session = orm.scoped_session(orm.sessionmaker())(bind=engine)
        blacklisted = json.loads(str(session.query(Projecteds).all()))
        #print(blacklisted)
        session.close()
        #print("Done Updating DB Blacklists")

async def projectedUpdater():
    global projecteds
    print("Starting Projected Updater")
    try:
        projecteds = await client.getProjected()
    except:
        await asyncio.sleep(60)
        projecteds = await client.getProjected()
    #After Itemsin Catalog
    print("Done init")
    while True:
        await asyncio.sleep(300)
        try:
            projecteds = await client.getProjected()
        except:
            await asyncio.sleep(60)
            projecteds = await client.getProjected()
        print("Finished Updating Projecteds!")

async def rapUpdater():
    #await asyncio.sleep(5)
    global rapDict
    global nameDict
    global projecteds
    print("Starting Rap Updater")
    try:
        raplist = await client.getRAP()
    except:
        await asyncio.sleep(60)
        raplist = await client.getRAP()
    #print(raplist)
    for assetidr, raplist2 in zip(raplist.keys(),raplist.values()):
        name = raplist2[0]
        rap = raplist2[2]
        rapDict[assetidr] = rap
        nameDict[assetidr] = name
    projecteds = await client.getProjected()
    #After Itemsin Catalog
    print("Done init")
    while True:
        await asyncio.sleep(1200)
        try:
            raplist = await client.getRAP()
        except:
            await asyncio.sleep(60)
            raplist = await client.getRAP()
        for assetidr, raplist2 in zip(raplist.keys(),raplist.values()):
            name = raplist2[0]
            rap = raplist2[2]
            rapDict[assetidr] = rap
            nameDict[assetidr] = name
        projecteds = await client.getProjected()
        print("Finished Updating Rap!")

async def DBUpdater():
    global instances
    print("Starting DB Updater!")
    session = orm.scoped_session(orm.sessionmaker())(bind=engine)
    instances = session.query(ActiveInstances).all()
    try:
        n = int(math.ceil(len(instances)/3))
        instances = [instances[i:i + n] for i in range(0, len(instances), n)]
        instances = instances[listnum]
        priorities = ast.literal_eval(str(session.query(Priorities).all()))
        temp = []
        temp2 = []
        for instance in instances:
            if str(instance.channelid) in priorities:
                temp.append(instance)
            else:
                temp2.append(instance)
        shuffle(temp)
        shuffle(temp2)
        instances = temp + temp2
    except:
        instances = []
    print(instances)
    for ins in instances:
        try:
            ins.xtoken=await client.setXsrfToken(ins.cookie)
            session.expire_on_commit = False
            session.commit()
        except:
            pass
    session.close()
    print("Done init")
    while True:
        await asyncio.sleep(20) #60
        session = orm.scoped_session(orm.sessionmaker())(bind=engine)
        instances = session.query(ActiveInstances).all()
        try:
            n = int(math.ceil(len(instances)/3))
            instances = [instances[i:i + n] for i in range(0, len(instances), n)]
            instances = instances[listnum]
            priorities = ast.literal_eval(str(session.query(Priorities).all()))
            temp = []
            temp2 = []
            for instance in instances:
                if str(instance.channelid) in priorities:
                    temp.append(instance)
                else:
                    temp2.append(instance)
            shuffle(temp)
            shuffle(temp2)
            instances = temp + temp2
        except:
            instances = []
        print(instances)
        for ins in instances:
            try:
                ins.xtoken=await client.setXsrfToken(ins.cookie)
                session.expire_on_commit = False
                session.commit()
            except:
                pass
        session.close()

async def versionUpdater():
    print("Starting Updater!")
    try:
        with open("info.ini", "r") as line_:
            for i in line_:
                version = int(base64.b64decode(i).decode("utf-8"))
                break
        url = ""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                if version != int(base64.b64decode(await r.text()).decode("utf-8")):
                    print("Updating!")
                    python = sys.executable
                    script = os.path.realpath("updater.pyc")
                    subprocess.Popen([python, script])
                    #os.execl(python, '"' + python + '"', "updater.pyc")
                    sys.exit()
                else:
                    print("No new versions found!")
    except Exception as e:
        print("Failed Updater", e)
    print("Done Init")
    while True:
        try:
            await asyncio.sleep(300)
            with open("info.ini", "r") as line_:
                for i in line_:
                    version = int(base64.b64decode(i).decode("utf-8"))
                    break
            url = ""
            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    if version != int(base64.b64decode(await r.text()).decode("utf-8")):
                        print("Updating!")
                        python = sys.executable
                        script = os.path.realpath("updater.pyc")
                        subprocess.Popen([python, script])
                        sys.exit()
                    else:
                        print("No new versions found!")
        except Exception as e:
            print("Failed Updater", e)


loopr = asyncio.get_event_loop()
loopr.create_task(rapUpdater())
loopr.create_task(projectedUpdater())
loopr.create_task(versionUpdater())
loopr.create_task(dbProjectedUpdater())
loopr.create_task(DBUpdater())

til = ti.split("-")
timeeeee = int(til[1]) - int(til[0]) + 1
i = int(til[0]) - 1
for index in range(timeeeee):
    i += 1
    loopr.create_task(itemUpdater(i))
#Real Bot
token = ""

loopr.create_task(bot.run(token))

loopr.run_forever()