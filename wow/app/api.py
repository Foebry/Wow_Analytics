"""api functionalities"""
from requesting.users import User
from requesting.security import oauth
from databases.Database import Database

import json


class API:

    def __init__(self, data):
        self.user = User(data["APP"])
        self.db = Database(data["DATABASE"])
        self.user.authenticate()


    def getItemData(self, item_id):
        """
            API call to request item data for specific item_id
        """
        endpoint = "item/{}".format(item_id)
        endpoint = self.user.endpoint.format(endpoint, "static", "", token=self.user.access_token)

        return self.user.get(endpoint)


    def getClassData(self, class_id):
        """
            API call to request class data for specific class_id
        """
        endpoint = "/item-class/{}".format(class_id)
        endpoint = self.user.endpoint.format(endpoint, "static", "", token=self.user.access_token)

        return self.user.get(endpoint)


    def getClassesIndex(self):
        """
            API call to request all item_classes.
        """
        endpoint = "item-class/index"
        endpoint = self.user.endpoint.format(endpoint, "static", "", token=self.user.access_token)

        return self.user.get(endpoint, ("item_classes",))


    def getSubclassData(self, class_id, subclass_id):
        """
            API call to request subclass data
        """
        endpoint = endpoint = "item-class/{}/item-subclass/{}".format(class_id, subclass_id)
        endpoint = self.user.endpoint.format(endpoint, "static", "", token=self.user.access_token)

        return self.user.get(endpoint)


    def getPetData(self, pet_id):
        """
            API call to request pet data
        """
        endpoint = "pet/{}".format(pet_id)
        endpoint = self.user.endpoint.format(endpoint, "static", "", token=self.user.access_token)

        return self.user.get(endpoint)


    def getMountData(self, mount_id):
        """
            API call to request mount data
        """
        endpoint = "mount/{}".format(mount_id)
        endpoint = self.user.endpoint.format(endpoint, "static", "", token=self.user.access_token)

        return self.user.get(endpoint)


    def getMount_id_by_name(self, name):
        """API call to get mount id by entering a mount name"""
        endpoint = "search/mount"
        extra = "&name.en_US={}&orderby=id&_page=1".format(name.replace(" ", "%20"))
        endpoint = self.user.endpoint.format(endpoint, "static", extra, token=self.user.access_token)

        results = self.user.get(endpoint, ("results",))

        for option in results:
            mount_name = option["data"]["name"]["en_GB"]
            mount_id = option["data"]["id"]

            if mount_name == name: return mount_id

        return False


    def getMountsIndex(self):
        """API call to get all mount indeces"""
        endpoint = "mount/index"
        endpoint = self.user.endpoint.format(endpoint, "static", "", token=self.user.access_token)

        return self.user.get(endpoint, ("mounts",))


    def getPetsIndex(self):
        """API call to retrieve all pet indeces"""
        endpoint = "pet/index"
        endpoint = self.user.endpoint.format(endpoint, "static", "", token=self.user.access_token)

        return self.user.get(endpoint, ("pets",))


    def getRealmData(self, condition):
        """API call to retrieve realm data for specific realm"""
        endpoint = "realm/index"
        endpoint = self.user.endpoint.format(endpoint, "dynamic", "", token=self.user.access_token)

        return self.user.get(endpoint, ("realms",), condition=condition)


    def getRealms(self):
        """API call to retrieve all realms"""
        endpoint = "search/realm"
        endpoint = self.user.endpoint.format(endpoint, "dynamic", "", token=self.user.access_token)

        pages = self.user.get(endpoint, ("pageCount",))
        result = []

        for page in range(pages):
            endpoint = "https://eu.api.blizzard.com/data/wow/search/realm?namespace=dynamic-eu&locale=en_GB&orderby=id&_page={}&access_token={}".format(page+1, self.user.access_token)
            response = self.user.get(endpoint, ("results",))

            result += response

        return result


    def getAuctionData(self, realm):
        """API call to request auction data for a specific realm"""
        endpoint = "connected-realm/{}/auctions".format(realm.id)
        endpoint = self.user.endpoint.format(endpoint, "dynamic", "", token=self.user.access_token)

        response = self.user.get(endpoint, raw=True)
        auctions = self.user.get(endpoint, ("auctions",))
        #print(data)
        if data:
            print("response:", "boop bap")
            if "last-modified" not in response.headers:
                from wow import wait
                wait(60)
                return self.getAuctionData(realm)
            if response.headers["last-modified"] == realm.last_modified:
                return []

            realm.last_modified = response.headers['last-modified']

            #if 'realms' in operation.update_data:
            #    operation.update_data["realms"].append(realm)
            return auctions


class Request():



    def getRegionRealms(self):
        """
            Method to extract all main realms from a certain region.
        """
        result = []
        realms = self.getRealms()

        for realm in realms:
            _id = realm["id"]
            pass
            # create realm
            # check realm for auction data
            # add realm if auction data exists



    def waitTillResponsive(unresponsive, args):
        import os

        ips = ('185.60.112.157', '185.60.112.158', '185.60.114.159')
        response = 0

        # already changed this section. Letting old code run to see which server will fail when server unresponsive.
        # response 0 means nothing wrong
        # response 1 meanse something wrong
        while unresponsive:
            for ip in ips: response += os.system("ping {}".format(ip))

            if response == 0: unresponsive = False
            response = 0


class Realm:
    def __init__(self, id_):
        self.id = id_
        self.last_modified = None

with open("config.json") as config:
    realm = Realm(1096)
    data = json.load(config)
    r = api(data)
    print(r.getAuctionData(realm)[:10])
    print(realm.last_modified)
