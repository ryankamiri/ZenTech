import json
import requests
import datetime
import time
import re
from threading import Thread
from bs4 import BeautifulSoup
import aiohttp
from fake_useragent import UserAgent
from aiohttp_proxy import ProxyConnector, ProxyType
from lxml.html import fromstring
import sys
import socket
import asyncio
#from selenium import webdriver
#import urllib.request

class Gear(object):
    def __init__(self):
        self.MELEE = 0
        self.RANGED = 1
        self.EXPLOSIVE = 2
        self.POWERUP = 3
        self.NAVIGATION = 4
        self.MUSICAL = 5
        self.SOCIAL = 6
class Subcategory(object):
    def __init__(self):
        self.FEATURED = 0
        self.ALL = 1
        self.COLLECTIBLES = 2
        self.CLOTHING = 3
        self.BODYPARTS = 4
        self.GEAR = 5
        self.MODELS = 6
        self.PLUGINS = 7
        self.DECALS = 8
        self.HATS = 9
        self.FACES = 10
        self.PACKAGES = 11
        self.SHIRTS = 12
        self.TSHIRTS = 13
        self.PANTS = 14
        self.HEADS = 15
        self.AUDIO = 16
        self.ROBLOXCREATED = 17
        self.MESHES = 18
class Genre(object):
    def __init__(self):
        self.ALL = 0
        self.TOWNANDCITY = 1
        self.MEDIEVAL = 2
        self.SCIFI = 3
        self.FIGHTING = 4
        self.HORROR = 5
        self.NAVAL = 6
        self.ADVENTURE = 7
        self.SPORTS = 8
        self.COMEDY = 9
        self.WESTERN = 10
        self.MILITARY = 11
        self.SKATING = 12
        self.BUILDING = 13
        self.FPS = 14
        self.RPG = 15
class Category(object):
    def __init__(self):
        self.FEATURED = 0
        self.ALL = 1
        self.COLLECTIBLES = 2
        self.CLOTHING = 3
        self.BODYPARTS = 4
        self.GEAR = 5
        self.MODELS = 6
        self.PLUGINS = 7
        self.DECALS = 8
        self.AUDIO = 9
        self.MESHES = 10
class Currency(object):
    def __init__(self):
        self.ALL = 0
        self.ROBUX = 1
        self.FREE = 2
class Sort(object):
    def __init__(self):
        self.RELEVANCE = 0
        self.MOSTFAVORITED = 1
        self.BESTSELLING = 2
        self.RECENTLYUPDATED = 3
        self.PRICELOWTOHIGH = 4
        self.PRICEHIGHTOLOW = 5
class Time(object):
    def __init__(self):
        self.PASTDAY = 0
        self.PASTWEEK = 1
        self.PASTMONTH = 2
        self.ALLTIME = 3

class RobloxApiClient(object):
    
    def __init__(self):
        self.s = requests.session()
        #self.token = {}
        # r = self.s.get("https://roblox.com/home")
        # tok = r.text[r.text.find("Roblox.XsrfToken.setToken('") + 27::]
        # tok = tok[:tok.find("');"):]
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0',
        #     'Accept': 'application/json, text/plain, */*',
        #     'Accept-Language': 'en-US,en;q=0.5',
        #     'Content-Type': 'application/json;charset=utf-8',
        #     'Origin': 'https://www.roblox.com',
        #     'X-CSRF-TOKEN': tok,
        #     'DNT': '1',
        # }
    def friends(self,id1,id2):
        t = self.s.get('https://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=IsFriendsWith&playerId='+id1+'&userId='+id2).text
        t=t.replace('<Value Type="boolean">','')
        t=t.replace('</Value>','')
        if t == 'true':
            return True
        else:
            return False
    def name(self,iyd):
        r = self.s.get('https://api.roblox.com/Users/'+iyd)
        jdict = json.loads(r.text)
        return jdict["Username"]

    def assetComments(self,id1):
        r = self.s.get('https://www.roblox.com/API/Comments.ashx?rqtype=getComments&assetID='+id1+'&startIndex=0')
        js = json.loads(r.text)
        return js
            
    async def catalogSearch(self,https_proxy,cookie,geartype = -1, genre = -1, subcategory = -1, category = -1, currency = -1, sort = -1, freq = -1, keyword = None, creatorID = None, minim = 0, maxim = None, notforsale = True, pagenumber = -1, resultsperpage = -1, url = False):
        cookies = {
                '.ROBLOSECURITY': cookie
            }
        async def search(cs):
            #try:
            if True:
                keyw = False
                req = 'https://search.roblox.com/catalog/json?'
                if geartype != -1:
                    req += '&Gears={}'.format(geartype)
                if genre != -1:
                    req += '&Genres={}'.format(genre)
                if subcategory != -1:
                    req += '&Subcategory={}'.format(subcategory)
                if category != -1:
                    req += '&Category={}'.format(category)
                if currency != -1:
                    req += '&CurrencyType={}'.format(currency)
                if sort != -1:
                    req += '&SortType={}'.format(sort)
                if freq != -1:
                    req += '&SortAggregation={}'.format(freq)
                if keyword != None:
                    req += '&Keyword={}'.format(keyword)
                    keyw = True
                if creatorID != None:
                    req += '&CreatorID={}'.format(creatorID)
                #req += '&PxMin={}'.format(minim)
                if maxim != None:
                    req += '&PxMax={}'.format(maxim)
                # if notforsale:
                #     req += '&IncludeNotForSale=true'
                # else:
                #     req += '&IncludeNotForSale=false'
                if pagenumber != -1:
                    if not keyw:
                        req +=  '&PageNumber={}'.format(pagenumber)
                if resultsperpage != -1:
                    req += '&ResultsPerPage={}'.format(resultsperpage)

                async with cs.get(req, cookies=cookies) as r:
                    try:
                    #if True:
                        #print(r.headers)
                        text = await r.json()
                        #print(text, "text")
                        if keyw:
                            for temp in text:
                                if temp.get("Name").lower() == keyword.lower():
                                    #print(temp.get("Name").lower(), keyword.lower())
                                    text = temp
                                    break
                        #print(text, "text")
                        return text
                    except Exception as e:
                        if r.status != 429:
                            print("-----")
                            print(e)
                            #if "Attempt to decode JSON with unexpected mimetype: text/html" in str(e):
                                #print(await r.text())
                            print(r.status)
                            print(req)
                            print("-----")
                        return None
            # except Exception as e:
            #     print(e, sys.exc_info()[-1].tb_lineno)
        # conn = aiohttp.TCPConnector(
        #     family=socket.AF_INET,
        #     verify_ssl=False,
        # )
        # sem = asyncio.Semaphore(100)
        # async with sem:
        async with aiohttp.ClientSession() as cs:
            result = await search(cs)
            return result

    def testcatalogSearch(self,https_proxy,cookie,geartype = -1, genre = -1, subcategory = -1, category = -1, currency = -1, sort = -1, freq = -1, keyword = None, creatorID = None, minim = 0, maxim = None, notforsale = True, pagenumber = -1, resultsperpage = -1, url = False):
        cookies = {
                '.ROBLOSECURITY': cookie
            }
        def search():
            #try:
            if True:
                keyw = False
                req = 'https://search.roblox.com/catalog/json?'
                if geartype != -1:
                    req += '&Gears={}'.format(geartype)
                if genre != -1:
                    req += '&Genres={}'.format(genre)
                if subcategory != -1:
                    req += '&Subcategory={}'.format(subcategory)
                if category != -1:
                    req += '&Category={}'.format(category)
                if currency != -1:
                    req += '&CurrencyType={}'.format(currency)
                if sort != -1:
                    req += '&SortType={}'.format(sort)
                if freq != -1:
                    req += '&SortAggregation={}'.format(freq)
                if keyword != None:
                    req += '&Keyword={}'.format(keyword)
                    keyw = True
                if creatorID != None:
                    req += '&CreatorID={}'.format(creatorID)
                #req += '&PxMin={}'.format(minim)
                if maxim != None:
                    req += '&PxMax={}'.format(maxim)
                # if notforsale:
                #     req += '&IncludeNotForSale=true'
                # else:
                #     req += '&IncludeNotForSale=false'
                if pagenumber != -1:
                    if not keyw:
                        req +=  '&PageNumber={}'.format(pagenumber)
                if resultsperpage != -1:
                    req += '&ResultsPerPage={}'.format(resultsperpage)


                r = requests.get(req, cookies=cookies)
                try:
                #if True:
                    #print(r.headers)
                    text = r.json()
                    #print(text, "text")
                    if keyw:
                        for temp in text:
                            if temp.get("Name").lower() == keyword.lower():
                                #print(temp.get("Name").lower(), keyword.lower())
                                text = temp
                                break
                    #print(text, "text")
                    return text
                except Exception as e:
                    if r.status_code != 429:
                        print("-----")
                        print(e)
                        #if "Attempt to decode JSON with unexpected mimetype: text/html" in str(e):
                            #print(await r.text())
                        print(r.status)
                        print(req)
                        print("-----")
                    return None
        result = search()
        return result

    def getFriends(self,userid):
        return self.s.get('https://api.roblox.com/users/'+str(userid)+'/friends').json()

    def friendCrawl(self,userid, maxfr = 100):
        usercount = 0
        users = []
        friendlist1 = getFriends(userid)       
        for friend in friendlist1:
            if len(users) < maxfr:
                if self.s.get('https://www.roblox.com/users/'+str(friend['Id'])+'/profile').status_code != 404:
                    users.append({'Id':friend['Id'],'Username':friend['Username']})
                    usercount += 1
                    print("Users: "+ str(usercount))
            else:
                return users
        for user in users:
            req = self.s.get("https://api.roblox.com/users/"+str(user['Id'])+"/friends")
            if req.status_code != 404:
                friendlist1 = json.loads(req.text)
            else:
                pass
            for friend in friendlist1:
                if len(users) < maxfr:
                    if self.s.get('https://www.roblox.com/users/'+str(friend['Id'])+'/profile').status_code != 404:
                        d = {'Id':friend['Id'],'Username':friend['Username']}
                        if d not in users:
                            users.append(d)
                            usercount += 1
                            print("Users: "+ str(usercount))
                else:
                    return users

    def getCurrentStatus(self):
        return self.s.get('https://www.roblox.com/client-status').text

    def getUserPresence(self,userid):
        return self.s.get('https://www.roblox.com/presence/user?userId={}'.format(userid)).json()
    
    def createAccount(self,username,password,birthday,gender = 2): #birthday is a datetime object
        params = {
            "isEligibleForHideAdsAbTest":False,
            "username":username,
            "password":password,
            "birthday": birthday.strftime("%d %b %Y").lstrip("0").replace(" 0", " "),
            "gender": gender, #3 for female, 2 for male
            "context":"RollerCoasterSignupForm"
        }
        print(params)
        r = self.s.post("https://api.roblox.com/signup/v1",data = params)
        return r

    async def getItemInfo(self,itemid, cookie):
        cookies = {
                '.ROBLOSECURITY': cookie
        }
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.roblox.com/marketplace/productinfo?assetId="+str(itemid), cookies=cookies) as r:
                try:
                    json = await r.json()
                    return json["ProductId"]
                except:
                    return None

    async def getProjected(self):
        async with aiohttp.ClientSession() as cs:
            ua = UserAgent()
            url = "https://www.rolimons.com/projecteditems"
            headers= {
                "Sec-Fetch-Dest": "document",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": ua.chrome
            }
            async with cs.get(url, headers=headers) as content:
                contentt = await content.text()

                for match in re.finditer(r'item_details\W=(.+?(?=;))', contentt, re.MULTILINE):
                    loaded = json.loads(match.group(1))
                    real = {}
                    for load in loaded:
                        data = loaded[load]
                        if data[5] == 1:
                            real.update({load: loaded[load]})
                    return real
    async def tbuyItem(self,itemid, cookie):
        #try:
        async with aiohttp.ClientSession() as cs:
            info = await self.getItemInfo(itemid, cookie)
            token = await self.setXsrfToken(cookie)
            #print(info)
            #url="https://api.roblox.com/item.ashx?rqtype=purchase&productID={}&expectedCurrency=1&expectedPrice={}&expectedSellerID={}&userAssetID=".format(info["ProductId"], 0 if info["PriceInRobux"] == None else info["PriceInRobux"],info["Creator"]["Id"])
            url="https://economy.roblox.com/v1/purchases/products/{}".format(info)
            #r = self.s.post(url, headers=XCSRFTOKEN)
            cookies = {
                '.ROBLOSECURITY': cookie
            }
            headers = {
                'X-CSRF-TOKEN': token
            }
            data = {}
            sellers = await self.getSellers(itemid, cookie)
            if sellers == None:
                return None
            #for seller in sellers['data']:
            seller = sellers['data'][0]
            data= {
                'expectedCurrency': 1, 'expectedPrice': seller['price'], 'expectedSellerId': seller['seller']['id'], 'userAssetID': seller['userAssetId']
                }
            if data == {}:
            #else:
                print("This item was already bought!")
                return False
            #r = self.s.post(url, data=data, cookies=cookies, headers=headers)
            async with cs.post(url, data=data, cookies=cookies, headers=headers) as r:
                #print(data, cookies, headers)
                #print(await r.json(), "json")
                json = await r.json()
                if json.get("errors") != None:
                    print(json, r.status)
                    if "Authorization" in str(json):
                        return None
                    if "Token" in str(json):
                        return "Incorrect Token"
                    return str(json)
                if json.get("purchased") == False:
                    print(json, r.status)
                    if json.get("reason") == "AlreadyOwned":
                        return "False3"
                    if json.get("reason") == "InsufficientFunds":
                        return "False2"
                    return False
                print("Bought Item!")
                #print(r.status_code)
                return True

    async def buyItem(self,itemid, cookie, price, token, ProductIds):
        async with aiohttp.ClientSession() as cs:
            url="https://economy.roblox.com/v1/purchases/products/{}".format(ProductIds)
            cookies = {
                '.ROBLOSECURITY': cookie
            }
            headers = {
                'X-CSRF-TOKEN': token
            }
            data = {}
            sellers = await self.getSellers(itemid, cookie)
            if sellers == None:
                return None
            seller = sellers['data'][0]
            if seller['price'] == price: 
                data= {
                    'expectedCurrency': 1, 'expectedPrice': seller['price'], 'expectedSellerId': seller['seller']['id'], 'userAssetID': seller['userAssetId']
                    }
            else:
                print("This item was already bought!")
                return False
            async with cs.post(url, data=data, cookies=cookies, headers=headers) as r:
                #print(data, cookies, headers)
                #print(await r.json(), "json")
                json = await r.json()
                if json.get("errors") != None:
                    print(json, r.status)
                    if "Authorization" in str(json):
                        return None
                    if "Token" in str(json):
                        return "Incorrect Token"
                    return str(json)
                if json.get("purchased") == False:
                    print(json, r.status)
                    if json.get("reason") == "AlreadyOwned":
                        return "False3"
                    if json.get("reason") == "InsufficientFunds":
                        return "False2"
                    return False
                print("Bought Item!")
                #print(r.status_code)
                return True
        # except Exception as e:
        #     print(f"Error on found snipe {e} {sys.exc_info()[-1].tb_lineno}")
    
    async def testbuyItem(self,itemid):
        async with aiohttp.ClientSession() as cs:
            url="https://economy.roblox.com/v1/purchases/products/{}".format(itemid)
            async with cs.post(url) as r:
                json = await r.json()
                return True

    def logIn(self,username,password,returnurl = ""):
        r = self.s.post("https://www.roblox.com/newlogin",data={"username":username,"password":password,"submitLogin":"Log In","ReturnUrl":returnurl})
        return r
    
    async def testcookie(self, cookie):
        # conn = aiohttp.TCPConnector(
        #     family=socket.AF_INET,
        #     verify_ssl=False,
        # )
        async with aiohttp.ClientSession() as cs:
            cookies = {
                '.ROBLOSECURITY': cookie
            }
            async with cs.get('https://www.roblox.com/game/GetCurrentUser.ashx', cookies=cookies) as r:
                if await r.text() != 'null':
                    return True
                else:
                    return False

    def giveBadge(self,userid,badgeid,placeid):
        return self.s.post("https://api.roblox.com/assets/award-badge", data = {'userId':userid,'badgeId':badgeid,'placeId':placeid}).json()
    
    def getVersions(self,itemid):
        return self.s.get("https://api.roblox.com/assets/{}/versions".format(itemid)).json()

    async def getCurrency(self, cookie):
        async with aiohttp.ClientSession() as cs:
            cookies = {
                '.ROBLOSECURITY': cookie
            }
            async with cs.get("https://api.roblox.com/currency/balance", cookies=cookies) as r:
                return await r.json()

    async def setXsrfToken(self, cookie):
        async with aiohttp.ClientSession() as cs:
            cookies = {
                '.ROBLOSECURITY': cookie
            }
            async with cs.get("https://roblox.com/home", cookies=cookies) as r:
                text = await r.text()
                tok = text[text.find("Roblox.XsrfToken.setToken('") + 27::]
                tok = tok[:tok.find("');"):]
                #self.token[cookie] = tok
                #print(tok)
                return tok

    def sendMessage(self,subject,body,recipientid):
        if not self.token:
            self.setXsrfToken()
        r = self.s.post('https://www.roblox.com/messages/send',headers = {'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8","X-CSRF-TOKEN":self.token}, data = {"subject":subject,"body":body,"recipientid":recipientid,"cacheBuster":round(time.time(),3)})
        return r

    def forumPost(self,forumid,subject,body,disablereplies = False): #currently nonfunctional
        earl = "https://forum.roblox.com/Forum/AddPost.aspx?ForumID={}".format(forumid)
        view = self.s.get(earl)
        soup = BeautifulSoup(view.text,'html.parser')
        params = {
            "__EVENTTARGET" : '',
            "__EVENTARGUMENT": '',
            '__VIEWSTATE':soup.find(id="__VIEWSTATE")['value'],
            "__VIEWSTATEGENERATOR":soup.find(id="__VIEWSTATEGENERATOR")['value'],
            "__EVENTVALIDATION" : soup.find(id="__EVENTVALIDATION")['value'],
            "ctl00$cphRoblox$Createeditpost1$PostForm$NewPostSubject":subject,
            "ctl00$cphRoblox$Createeditpost1$PostForm$PostBody":body,
            "ctl00$cphRoblox$Createeditpost1$PostForm$PostButton":" Post "
        }
        if disablereplies:
            params["ctl00$cphRoblox$Createeditpost1$PostForm$AllowReplies"] = 'on'
        r = self.s.post(earl, data = params, headers = {"Content-Type":"application/x-www-form-urlencoded"})
        return r

    def replyToForumPost(self, postid, text, disablereplies = False):
        earl = "https://forum.roblox.com/Forum/AddPost.aspx?PostID={}".format(postid)
        view = self.s.get(earl)
        soup = BeautifulSoup(view.text,'html.parser')
        params = {
            "__EVENTTARGET" : '',
            "__EVENTARGUMENT": '',
            '__VIEWSTATE':soup.find(id="__VIEWSTATE")['value'],
            "__VIEWSTATEGENERATOR":soup.find(id="__VIEWSTATEGENERATOR")['value'],
            "__EVENTVALIDATION" : soup.find(id="__EVENTVALIDATION")['value'],
            "ctl00$cphRoblox$Createeditpost1$PostForm$PostBody":text,
            "ctl00$cphRoblox$Createeditpost1$PostForm$PostButton":" Post "
        }
        if disablereplies:
            params["ctl00$cphRoblox$Createeditpost1$PostForm$AllowReplies"] = 'on'
        r = self.s.post(earl, data = params, headers = {"Content-Type":"application/x-www-form-urlencoded"})
        return r

    
    def getRobloSecurityCookie(self):
        return self.s.cookies.get_dict()['.ROBLOSECURITY']

    def commentOnAsset(self,assetid,text):
        if not self.token:
            self.setXsrfToken()
        r = self.s.post("https://www.roblox.com/comments/post",data = {'assetId':assetid,'text':text}, headers = {"X-CSRF-TOKEN":self.token})
        return r
    
    def joinGroup(self,groupid):
        viewpage = self.s.get("https://www.roblox.com/groups/group.aspx?gid={}".format(groupid))
        soup = BeautifulSoup(viewpage.text,'html.parser')
        params = {
        '__EVENTTARGET':"JoinGroupDiv",
        '__EVENTARGUMENT':"Click",
        '__LASTFOCUS':'',
        '__VIEWSTATE':soup.find(id="__VIEWSTATE")['value'],
        '__VIEWSTATEGENERATOR':soup.find(id="__VIEWSTATEGENERATOR")['value'],
        '__EVENTVALIDATION':soup.find(id="__EVENTVALIDATION")['value'],
        'ctl00$cphRoblox$GroupSearchBar$SearchKeyword':"Search all groups",
        'ctl00$cphRoblox$rbxGroupRoleSetMembersPane$dlRolesetList':soup.find(id="ctl00_cphRoblox_rbxGroupRoleSetMembersPane_dlRolesetList").find(selected="selected")['value'],
        'ctl00$cphRoblox$rbxGroupRoleSetMembersPane$RolesetCountHidden':soup.find(id="ctl00_cphRoblox_rbxGroupRoleSetMembersPane_RolesetCountHidden")['value'],
        'ctl00$cphRoblox$rbxGroupRoleSetMembersPane$dlUsers_Footer$ctl01$PageTextBox':soup.find(id="ctl00_cphRoblox_rbxGroupRoleSetMembersPane_dlUsers_Footer_ctl01_PageTextBox")['value'],
        'ctl00$cphRoblox$rbxGroupRoleSetMembersPane$currentRoleSetID':soup.find(id="ctl00_cphRoblox_rbxGroupRoleSetMembersPane_currentRoleSetID")['value']
        }
        r = self.s.post("https://www.roblox.com/groups/group.aspx?gid={}".format(groupid), data = params, headers = {'Content-Type':'application/x-www-form-urlencoded'})
        return r

    def reportAbuse(self,userid,category,comment):
        view = self.s.get("https://www.roblox.com/abusereport/UserProfile?id={}".format(userid))
        params = {
        '__RequestVerificationToken':re.search('name="__RequestVerificationToken" type="hidden" value="(.+)"',view.text).group(1),
        'ReportCategory':category,
        'Comment':comment,
        'Id':userid,
        'RedirectUrl':'/Login',
        'PartyGuid':'',
        'ConversationId':''
        }
        r = self.s.post("https://www.roblox.com/abusereport/UserProfile?id={}",data=params)
        return r

    async def oldgetRAP(self,aid,name,cookie,returnv = None):
        # async def get_proxies():
        #     url = 'https://free-proxy-list.net/'
        #     #response = requests.get(url)
        #     async with aiohttp.ClientSession() as cs:
        #         async with cs.get(url) as response:
        #             parser = fromstring(await response.text())
        #             proxies = []
        #             for i in parser.xpath('//tbody/tr')[:10]:
        #                 #if i.xpath('.//td[7][contains(text(),"yes")]'):
        #                 proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
        #                 proxies.append(proxy)
        #     return proxies


        async with aiohttp.ClientSession() as cs:
            try:
                cookies = {
                    '.ROBLOSECURITY': cookie
                }

                url = f"https://www.roblox.com/catalog/{aid}/{name}"
                browser = webdriver.PhantomJS(executable_path='C:\\dev\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
                browser.get(url)
                html = browser.page_source
                soup = BeautifulSoup(html, 'lxml')
                a = soup.find("span", {"id": "item-average-price"})
                #print(a.text)
                return(a.text)

                    # html = response.read().decode('utf-8')
                    # soup = BeautifulSoup(html, "html.parser")
                    # for headline in soup.find_all("span", {"id": "item-average-price"}):
                    #     print(headline.text)
                    #     return headline.text

                # async with cs.get(f"https://www.roblox.com/catalog/16984917/Gearloose-Goggles", cookies=cookies) as txt:
                #     soup = BeautifulSoup(await txt.text(), "html.parser")
                #     print(txt.status)
                #     with open('test.txt', 'w+') as file:
                #         file.write(await txt.text())
                #     #print(soup)
                #     #print(soup.find_all("div"))
                #     print(soup.find_all('span', class_ = 'text-robux ng-binding'))
                #     for headline in soup.find_all("span", {"id": "item-average-price"}):
                #         print(headline.text)
                #         return headline.text
                    

                    # parser = fromstring(await txt.text())
                    # #print(parser)
                    # print(parser.xpath("//body"))
                    # for i in parser.xpath("//body"):
                    #     print(i)
                    #txt = await txt.json()

                    
                    #print(txt)
            #         try:
            #             value = txt['recentAveragePrice']
            #         except Exception as e:
            #             print(e)
            #             print(txt)
            #             return False
            #         if returnv:
            #             returnv[0] += value
            #         else:
            #             return value
            except Exception as e:
                print(e)
                return False


    async def oldoldgetRAP(self,aid,returnv = None):

        # async with aiohttp.ClientSession(connector=connecotr) as cs:
        #     #async with cs.head("https://economy.roblox.com/v1/assets/{}/resale-data".format(aid)) as x:
        #     if True:
        #         x = requests.head("https://economy.roblox.com/v1/assets/57028494/resale-data")
        #         print(x.status_code)
        #         print(x.raw.__dict__)

        async with aiohttp.ClientSession() as cs:
            try:
                async with cs.get("https://economy.roblox.com/v1/assets/{}/resale-data".format(aid), proxy="http://50.233.228.147:8080") as txt:
                    #print(txt.headers)
                    #print(txt.body)
                    
                    txt = await txt.json()

                    
                    #print(txt)
                    try:
                        value = txt['recentAveragePrice']
                    except Exception as e:
                        print(e)
                        print(txt)
                        return False
                    if returnv:
                        returnv[0] += value
                    else:
                        return value
            except Exception as e:
                print(e)
                return False
    
    async def getRRAP(self,aid,returnv = None):
        async with aiohttp.ClientSession() as cs:
            ua = UserAgent()
            headers= {
                "Sec-Fetch-Dest": "document",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": ua.chrome
            }
            async with cs.get(f'https://www.rolimons.com/item/{aid}', headers=headers) as content:
                contentt = await content.text()
                soup = BeautifulSoup(contentt, "lxml")
                rap = soup.findAll("h5", {"class": "card-title mb-1 text-light text-truncate stat-data"})
                rap = str(rap[1])
                
                #print(rap, "Here")
                temp = rap.split(">")
                #print(temp, "d")
                rap = temp[1]
                #print(rap, "d")
                temp = rap.split("<")
                rap = temp[0]

                rap = int(rap.replace(',', ''))
                print(rap, "fake")
                return rap
                    
    async def get2ndRAP(self,aid,returnv = None):
        async with aiohttp.ClientSession() as cs:
            try:
                async with cs.get("https://economy.roblox.com/v1/assets/{}/resale-data".format(aid)) as txt:
                    #print(sys.getsizeof(txt))
                    #print(txt.headers.get("content-length"))
                    #print(txt.headers)
                    #print(txt.body)
                    
                    txt = await txt.json()
                    #print(txt)
                    
                    #print(txt)
                    try:
                        value = txt['recentAveragePrice']
                    except Exception as e:
                        print(e)
                        print(txt)
                        return False
                    if returnv:
                        returnv[0] += value
                    else:
                        return value
            except Exception as e:
                print(e)
                return False
    
    async def getRAP(self,returnv = None):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.rolimons.com/itemapi/itemdetails") as r:
                r = await r.json()
                #print(r)
                value = r['items']
                return value

    def getUserRAP(self,uid):
        hats = self.s.get("https://www.roblox.com/users/inventory/list-json?assetTypeId=8&cursor=&itemsPerPage=999999&pageNumber=1&userId={}".format(uid)).json()
        gear = self.s.get("https://www.roblox.com/users/inventory/list-json?assetTypeId=19&cursor=&itemsPerPage=999999&pageNumber=1&userId={}".format(uid)).json()
        faces = self.s.get("https://www.roblox.com/users/inventory/list-json?assetTypeId=18&cursor=&itemsPerPage=999999&pageNumber=1&userId={}".format(uid)).json()
        hatlist = []
        gearlist = []
        facelist = []
        if hats['IsValid'] == False:
            return None
        for hat in hats['Data']['Items']:
            try:
                if hat['Product'] and hat['Product']['IsLimited'] or hat['Product']['IsLimitedUnique']:
                    hatlist.append(hat['Item']['AssetId'])
            except TypeError as e:
                pass
        for hat in gear['Data']['Items']:
            try:
                if hat['Product'] and hat['Product']['IsLimited'] or hat['Product']['IsLimitedUnique']:
                    gearlist.append(hat['Item']['AssetId'])
            except TypeError as e:
                pass
        for hat in faces['Data']['Items']:
            try:
                if hat['Product'] and hat['Product']['IsLimited'] or hat['Product']['IsLimitedUnique']:
                    facelist.append(hat['Item']['AssetId'])
            except TypeError as e:
                pass
        threadarr = []
        returnval = [0]
        for item in hatlist+gearlist+facelist:
            threadarr.append(Thread(target=self.getRAP,args=(item,returnval)))
        for thread in threadarr:
            thread.start()
        for thread in threadarr:
            thread.join()
        return returnval[0]

    async def getSellers(self,aid,cookie):
        #r = requests.get("https://www.roblox.com/asset/resellers?productId={}&startIndex=0&maxRows=9999999".format(self.getItemInfo(aid)['ProductId']))
        async with aiohttp.ClientSession() as cs:
            cookies = {
                '.ROBLOSECURITY': cookie
            }
            url = "https://economy.roblox.com/v1/assets/{}/resellers".format(aid)
            async with cs.get(url, cookies=cookies) as r:
                json = await r.json()
                if "Authorization" in str(json) and "errors" in str(json):
                    print("Invalid Cookie")
                    return None
                return json

    def getSalesData(self,aid):
        return requests.get("https://www.roblox.com/asset/{}/sales-data".format(aid)).json()

    def snipeLimited(self,aid,desiredprice):
        self.token = requests.post("https://web.roblox.com/api/item.ashx?rqtype=purchase&productID={}&expectedCurrency=1&expectedPrice={}&expectedSellerID={}&userAssetID={}").headers['X-CSRF-TOKEN']
        sellers = self.getSellers(aid)
        for seller in sellers['data']['Resellers']:
            if seller['Price'] <= desiredprice:
                return requests.post("https://web.roblox.com/api/item.ashx?rqtype=purchase&productID={}&expectedCurrency=1&expectedPrice={}&expectedSellerID={}&userAssetID={}".format(self.getItemInfo(aid)['ProductId'],seller['Price'],seller['SellerId'],seller['UserAssetId']),headers = {"X-CSRF-TOKEN":self.token})
        return False

    def logOut(self):
        if not self.token:
            self.setXsrfToken()
        r = self.s.post("https://api.roblox.com/sign-out/v1",headers={'X-CSRF-TOKEN':self.token})
        return r

    def favItem(self,itemid) : # made by Vibe
        if not self.token:
            self.setXsrfToken()
        r = self.s.post('https://www.roblox.com/favorite/toggle', data = {'assetid': itemid,'isguest' : 'false'}, headers = {"X-CSRF-TOKEN":self.token})
        return r
    def updateStatus(self, message) : # also made by Vibe
        if not self.token:
            self.setXsrfToken()
        r = self.s.post('https://www.roblox.com/home/updatestatus', data = {'status': message}, headers = {"X-CSRF-TOKEN":self.token})
        return r
    
    def sendVerEmail(self):
        r=self.s.post('https://www.roblox.com/my/account/sendverifyemail')
        return r

    def getLeaderBoard(self,gid):
        git = self.s.get('https://www.roblox.com/--item?id={}'.format(gid))
        text=git.text
        reg = re.search("data-distributor-target-id=\"(.+)\"\s*data-max=\"(.+)\"\s*data-rank-max=\"(.+)\"\s*data-target-type=\"(.+)\"\s*data-time-filter=\"(.+)\"\s*data-player-id=\"(.+)\"\s*data-clan-id=\"(.+).></div>",text)
        if reg:
            data={
            'targetType': reg.group(4),
            'distributorTargetId': reg.group(1),
            'timeFilter': reg.group(5),
            'startIndex': 0,
            'currentRank': 1,
            'previousPoints': - 1,
            'max': reg.group(2),
            'imgWidth': 48,
            'imgHeight': 48,
            'imgFormat': 'PNG'
          }
            r= requests.get('https://roblox.com/leaderboards/rank/json',params=data)
            return r
        else:
            return None
## do stuff
