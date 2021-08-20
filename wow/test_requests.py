import unittest
import os


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
        db = Database(db_data, logger)
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


    @unittest.skip ("no need if test_init works")
    def test_setEndpoint(self):
        request.setAccessToken()
        self.assertEqual("https://eu.api.blizzard.com/data/wow/{}?namespace={}-eu&locale=en_GB{}&access_token=%s"%request.access_token, request.setEndpoint())

    @unittest.skip ("no need if test_init works")
    def test_setAccessToken(self):
        request.setAccessToken()
        self.assertEqual(str, type(request.access_token))


    @unittest.skip
    def test_getAuctionData(self):
        from operations import Operation
        operation = Operation(db, logger)

        request.getAuctionData()


    @unittest.skip
    def test_getItemData(self):
        pass


    @unittest.skip
    def test_getClassData(self):
        pass

    @unittest.skip
    def test_getClassIndex(self):
        pass

    @unittest.skip
    def test_getSubClassData(self):
        pass

    @unittest.skip
    def test_getPetData(self):
        pass

    @unittest.skip
    def test_getMountData(self):
        pass

    @unittest.skip
    def test_getMount_id_by_name(self):
        pass

    @unittest.skip
    def test_getMountsIndex(self):
        pass

    @unittest.skip
    def test_getPetsIndex(self):
        pass


    def test_getRealmData(self):
        data = request.getRealmData(("id", 1096))

        self.assertEqual(dict, type(data))
        self.assertEqual(True, "name" in data)
        self.assertEqual(True, "id" in data)
        self.assertEqual(True, "slug" in data)
        self.assertEqual("Scarshield Legion", data["name"])
        self.assertEqual(1096, data["id"])
        self.assertEqual("scarshield-legion", data["slug"])


    @unittest.skip
    def test_getRealms(self):
        pass

    @unittest.skip
    def test_reconnect(self):
        pass

    @unittest.skip
    def test_waitTillResponsive(self):
        pass

    @unittest.skip
    def test_handleResponse(self):
        pass

    @unittest.skip
    def test_travelResponse(self):
        pass

    @unittest.skip
    def test_searchResponse(self):
        pass


if __name__ == "__main__":
    data, db, logger, request, operation = RequestTest.init()
    unittest.main()
