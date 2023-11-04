import requests, random, time, heapq, colorama, json
from colorama import Fore, Back, Style
colorama.init(autoreset=True)



totalTradeAds = 0
while True:
    try:
        with open("config.json") as jsonfile:
            config = json.load(jsonfile)
            userID = config["UserID"]
            RoliVerification = config["RoliVerification"]
            wait = config["Wait"]
            realstic = config["Realstic"]

        itemsIds = []
        itemRaps = []
        nextPageCursor = None
        while True:
            params={"cursor": nextPageCursor}
            getData = requests.get(f"https://inventory.roblox.com/v1/users/{userID}/assets/collectibles",params=params).json()
            nextPageCursor = getData["nextPageCursor"]

            for item in getData["data"]:
                rap = item["recentAveragePrice"]
                itemID = item["assetId"]
                if rap == None:
                    pass
                else:
                    itemsIds.append(itemID)
                    itemRaps.append(rap)
            if nextPageCursor == None:
                break

        if len(itemsIds) >= 4:
            itemsToSort = 4
        else:
            itemsToSort = len(itemsIds)
        sort = heapq.nlargest(itemsToSort, zip(itemRaps, itemsIds))

        offerIds = []
        for item in sort:
            itemID = item[1]
            offerIds.append(itemID)

        cookie = {"_RoliVerification": RoliVerification}
        payload = {"player_id":userID,"offer_item_ids":offerIds,"request_item_ids":[],"request_tags":["demand","upgrade","downgrade"]}

        postAd = requests.post("https://www.rolimons.com/tradeapi/create", json=payload, cookies=cookie)

        if realstic == True:
            randomWait = random.randint(1,250)
        else:
            randomWait = 0
        randomWait = randomWait + wait

        if postAd.status_code == 201:
            totalTradeAds+=1
            print(Fore.GREEN+f"[!] Succesfull Made A Trade Ad With The Item IDs", Fore.CYAN+str(offerIds), Fore.GREEN+"Total Trade Ads", Fore.CYAN+str(totalTradeAds), Fore.GREEN+"Waiting", Fore.CYAN+str(randomWait), Fore.GREEN+"Secends")
        else:
            print(Fore.RED+f"[?] Failed To Post Trade Ad With The Item Ids", Fore.CYAN+str(offerIds), Fore.RED+"Total Trade Ads", Fore.CYAN+str(totalTradeAds), Fore.RED+"Waiting", Fore.CYAN+str(randomWait), Fore.RED+"Secends")

        time.sleep(randomWait)
    except:
        print("error with web SMH")

