import unittest
import os

from operations import *

class OperationTest(unittest.TestCase):

    @staticmethod
    def init():
        from databases.Database import Database
        from logger.Logger import Logger
        from config import DATABASE as data
        from mounts import Mount
        from pets import Pet
        from classes import Class, Subclass
        from items import Item
        from auctions import Auction, Soldauction

        logger = Logger(os.getcwd())
        db = Database(data, logger, test=True)
        operation = Operation(db, logger)

        data = {"mounts":[], "pets":[], "classes":[], "subclasses":[],
                "items":[], "auctions":[], "soldauctions":[]}

        data["mounts"] = [Pet(_id) for _id in (1,2)]
        data["pets"] = [Pet(_id) for _id in (1, 2)]
        data["classes"] = [Class(_id) for _id in (1, 2)]
        data["subclasses"] = [Subclass(_id, 1) for _id in (1, 2)]
        data["items"] = [Item(_id) for _id in (1, 2)]
        data["auctions"] = [Auction()]
        data["soldauctions"] = [Soldauction()]


        return db, logger, operation, data


    def test_init(self):
        self.assertEqual(db, operation.database)
        self.assertEqual(logger, operation.logger)
        self.assertEqual({}, operation.insert_data)
        self.assertEqual({}, operation.update_data)
        self.assertEqual({}, operation.live_data)
        self.assertEqual([], operation.realms)


    @unittest.skip
    def test_insertData(self):
        pass


    @unittest.skip
    def test_updateData(self):
        pass


    @unittest.skip
    def test_setLiveMount(self):
        pass


    @unittest.skip
    def test_setLivePets(self):
        pass


    @unittest.skip
    def test_setLiveClasses(self):
        pass


    @unittest.skip
    def test_setLiveSubclasses(self):
        pass


    @unittest.skip
    def test_setLiveItems(self):
        pass


    @unittest.skip
    def test_setLiveAuction(self):
        pass


    @unittest.skip
    def test_setLiveData(self):
        pass



    def test_update(self):
        operation.update()
        self.assertEqual({}, operation.insert_data)
        self.assertEqual({}, operation.update_data)


    @unittest.skip
    def test_setTimePosted(self):
        pass


    @unittest.skip
    def test_setTimeSold(self):
        pass


if __name__ == "__main__":
    db, logger, operation, data = OperationTest.init()
    unittest.main()
