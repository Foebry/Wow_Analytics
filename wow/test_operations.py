import unittest
import os

from operations import *

class OperationTest(unittest.TestCase):

    @staticmethod
    def init():
        from databases.Database import Database
        from logger.Logger import Logger
        from config import DATABASE as data

        logger = Logger(os.getcwd())
        db = Database(data, logger)
        operation = Operation(db, logger)

        return db, logger, operation


    def test_init(self):
        self.assertEqual(db, operation.database)
        self.assertEqual(logger, operation.logger)
        self.assertEqual({}, operation.insert_data)
        self.assertEqual({}, operation.update_data)
        self.assertEqual({}, operation.live_data)
        self.assertEqual([], operation.realms)


    @unittest.skip
    def test_setRegionRealms(self):
        pass


    @unittest.skip
    def test_updateData(self):
        pass


    @unittest.skip
    def test_insertData(self):
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


    @unittest.skip
    def test_update(self):
        pass


    @unittest.skip
    def test_setTimePosted(self):
        pass


    @unittest.skip
    def test_setTimeSold(self):
        pass


if __name__ == "__main__":
    db, logger, operation = OperationTest.init()
    unittest.main()
