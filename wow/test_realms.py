import unittest
import os

from realms import *

print("test_realms")


class RealmTest(unittest.TestCase):

    @staticmethod
    def init():
        from databases.Database import Database
        from logger.Logger import Logger
        from Requests import Request
        from config import DATABASE as db_data, CREDENTIALS as data

        logger = Logger(os.getcwd())
        db = Database(db_data, logger, test=True)
        request = Request(data, db, logger)
        store = [True, False, True]
        region = [True, False, False]
        indices = [0, 506, 1096]
        realms = [Realm(indices[x], db, logger, request, store[x], region[x]) for x in range(3)]

        return realms, db, logger, request



    def test_init(self):
        realm = realms[2]

        # testing realm to store data
        self.assertEqual(1096, realm.id)
        self.assertEqual("Scarshield Legion", realm.name)
        self.assertEqual("D://Games//World of Warcraft//_retail_//Interface//AddOns//wow_analytics//scarshield-legion.lua", realm.output)
        self.assertEqual(True, realm.store)
        self.assertEqual(db, realm.database)
        self.assertEqual(logger, realm.logger)
        self.assertEqual({}, realm.auctions)
        self.assertEqual({}, realm.previous_auctions)
        self.assertEqual(None, realm.last_modified)

        # testing realm not to store data
        realm = realms[1]

        self.assertEqual("Draenor", realm.name)
        self.assertEqual(None, realm.output)
        self.assertEqual(False, realm.store)
        self.assertEqual(None, realm.last_modified)

        # testing region realm
        realm = realms[0]

        self.assertEqual("Region", realm.name)
        self.assertEqual("D://Games//World of Warcraft//_retail_//Interface//AddOns//wow_analytics//region.lua", realm.output)
        self.assertEqual(True, realm.store)
        self.assertEqual(None, realm.last_modified)

        # testing insert
        data = db.get("Select * from responses", all=True)
        self.assertEqual(3, len(data))
        self.assertEqual(realms[0].id, data[0][0])
        self.assertEqual(realms[1].id, data[1][0])
        self.assertEqual(realms[2].id, data[2][0])

        db.execute("delete from responses")


    @unittest.skip("being tested in test_init")
    def test_setOutputFile(self):
        realm = realms[0]
        self.assertEqual(realm.output, realm.setOutputFile(request, realm.region))



    def test_insert(self):
        realm = realms[2]
        realm.insert()
        data = db.get("select * from responses", all=True)

        self.assertEqual(1, len(data))
        self.assertEqual(realm.id, data[0][0])



    def test_update(self):
        from datetime import datetime

        now = str(datetime.now())
        realm = realms[2]
        realm.last_modified = now
        realm.update()

        data = db.get("select previous_response from responses where realm_id = {}".format(realm.id))
        self.assertEqual(now, data[0])

        db.execute("delete from responses")



    @unittest.skip
    def test_exportAuctionData(self):
        pass


    @unittest.skip
    def test_setAuctionData(self):
        pass


if __name__ == "__main__":
    realms, db, logger, request = RealmTest.init()
    unittest.main()
