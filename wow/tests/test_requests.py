import unittest
import os

print("test_requests")


class RequestTest(unittest.TestCase):

    @staticmethod
    def init():
        from logger.Logger import Logger
        from databases.Database import Database
        from operations import Operation
        from config import DATABASE as db_data
        from Requests import Request
        from config import CREDENTIALS as data

        logger = Logger(os.getcwd())
        db = Database(db_data, logger, test=True, testcase=True)
        request = Request(data, db, logger)
        operation = Operation(db, logger)

        return data, db, logger, request, operation



    def test_init(self):
        self.assertEqual(data["client_id"], request.client_id)
        self.assertEqual(data["client_secret"], request.client_secret)
        self.assertEqual(request.setAccessToken(), request.access_token)
        self.assertEqual(request.setEndpoint(), request.endpoint)
        self.assertEqual(db, request.database)
        self.assertEqual(logger, request.logger)


    def test_setEndpoint(self):
        request.setAccessToken()
        self.assertEqual("https://eu.api.blizzard.com/data/wow/{}?namespace={}-eu&locale=en_GB{}&access_token=%s"%request.access_token, request.setEndpoint())


    def test_setAccessToken(self):
        self.assertEqual(request.setAccessToken(), request.access_token)
        self.assertEqual(str, type(request.access_token))


    def test_getAuctionData(self):
        from realms import Realm

        realm_id = 1096
        realm = Realm(realm_id, db, logger, request)

        response = request.getAuctionData(realm, operation)
        self.assertEqual(list, type(response))


    def test_getItemData(self):
        item_id = 37
        response = request.getItemData(item_id)

        self.assertEqual(dict, type(response))
        self.assertEqual(True, "id" in response)
        self.assertEqual(True, "name" in response)
        self.assertEqual(item_id, response["id"])
        self.assertEqual("Worn Axe", response["name"])



    def test_getClassData(self):
        class_id = 0
        response = request.getClassData(class_id)

        self.assertEqual(dict, type(response))
        self.assertEqual(True, "class_id" in response)
        self.assertEqual(True, "name" in response)
        self.assertEqual(class_id, response["class_id"])
        self.assertEqual("Consumable", response["name"])


    def test_getClassesIndex(self):
        response = request.getClassesIndex()

        self.assertEqual(list, type(response))
        self.assertEqual(17, len(response))


    def test_getSubClassData(self):
        class_id = 0
        subclass_id = 0
        response = request.getSubclassData(class_id, subclass_id)

        self.assertEqual(dict, type(response))
        self.assertEqual(True, "display_name" in response)
        self.assertEqual(True, "class_id" in response)
        self.assertEqual(True, "subclass_id" in response)
        self.assertEqual("Explosives and Devices", response["display_name"])
        self.assertEqual(class_id, response["class_id"])
        self.assertEqual(subclass_id, response["subclass_id"])


    def test_getPetData(self):
        pet_id = 39
        response = request.getPetData(pet_id)

        self.assertEqual(dict, type(response))
        self.assertEqual(True, "id" in response)
        self.assertEqual(True, "name" in response)
        self.assertEqual(pet_id, response["id"])
        self.assertEqual("Mechanical Squirrel", response["name"])


    def test_getMountData(self):
        mount_id = 985
        response = request.getMountData(mount_id)

        self.assertEqual(dict, type(response))
        self.assertEqual(True, "id" in response)
        self.assertEqual(True, "name" in response)
        self.assertEqual(mount_id, response["id"])
        self.assertEqual("Avenging Felcrusher", response["name"])



    def test_getMount_id_by_name(self):
        mount_name = "Avenging Felcrusher"
        response = request.getMount_id_by_name(mount_name)

        self.assertEqual(985, response)


    def test_getMountsIndex(self):
        response = request.getMountsIndex()

        self.assertEqual(list, type(response))
        self.assertEqual("Brown Horse", response[0]["name"])
        self.assertEqual(6, response[0]["id"])


    def test_getPetsIndex(self):
        response = request.getPetsIndex()

        self.assertEqual(list, type(response))
        self.assertEqual("Mechanical Squirrel", response[0]["name"])
        self.assertEqual(39, response[0]["id"])


    def test_getRealmData(self):
        data = request.getRealmData(("id", 1096))

        self.assertEqual(dict, type(data))
        self.assertEqual(True, "name" in data)
        self.assertEqual(True, "id" in data)
        self.assertEqual(True, "slug" in data)
        self.assertEqual("Scarshield Legion", data["name"])
        self.assertEqual(1096, data["id"])
        self.assertEqual("scarshield-legion", data["slug"])



    def test_getRealms(self):
        response = request.getRealms()

        self.assertEqual(list, type(response))
        self.assertEqual(267, len(response))
        self.assertEqual("Aggramar", response[0]["data"]["name"]["en_GB"])
        self.assertEqual(500, response[0]["data"]["id"])



if __name__ == "__main__":
    data, db, logger, request, operation = RequestTest.init()
    unittest.main()
