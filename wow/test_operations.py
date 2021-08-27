import unittest
import os

from databases.Database import Database
from logger.Logger import Logger
from config import DATABASE, CREDENTIALS
from Requests import Request
from operations import Operation
from realms import Realm

class OperationTest(unittest.TestCase):

    @staticmethod
    def init(section=None):
        from mounts import Mount
        from pets import Pet
        from classes import Class, Subclass
        from items import Item
        from auctions import Auction, SoldAuction
        from datetime import datetime


        if section == "insert":
            operation.realms = [realm,]
            operation.live_data = {"auctions":{realm.id:{}}, "items":{82800:{}}, "classes":{}, "subclasses":{}, "pets":{}, "mounts":{}}
            [Mount(operation, request, _id) for _id in (69, 85)]
            [Pet(operation, request, _id) for _id in (39, 40)]

            time = datetime.now()
            auction_1 = Auction(realm, operation, request, False, *(realm, 10569, 25, {"_id":0}, 1, 52, "SHORT", 24.9, 52, time, time))
            time = datetime.now()
            auction_2 = Auction(realm, operation, request, False, *(realm, 10570, 35, {"_id":0}, 1, 68, "MEDIUM", 62.5, 68, time, time))

            operation.insert_data["auctions"][realm.id] = [auction_1, auction_2]
            operation.live_data["auctions"][realm.id] = {10569:auction_1, 10570:auction_2}

            time = datetime.now()
            sold_auction = SoldAuction(operation, *(auction_2, 10570, 35, {"id":0}, 1, 68, "MEDIUM", 62.5, 68, auction_2.time_posted, False))
            operation.insert_data["sold_auctions"][realm.id] = [sold_auction]

        elif section == "update":
            operation.update_data = {"auctions":{}}
            time = datetime.now()
            item = operation.live_data["items"][25]
            auction = operation.live_data["auctions"][realm.id][10569]
            auction.last_updated = time
            item.mean_price = 1


            operation.update_data["items"] = [item,]
            operation.update_data["auctions"][realm.id] = [auction,]


    def test_init(self):
        self.assertEqual(db, operation.database)
        self.assertEqual(logger, operation.logger)
        self.assertEqual({"items":[], "classes":[], "subclasses":[], "pets":[], "mounts":[], "item_prices":[]}, operation.insert_data)
        self.assertEqual({}, operation.update_data)
        self.assertEqual({"items":{82800:{}}, "classes":{}, "pets":{}, "mounts":{}}, operation.live_data)
        self.assertEqual([], operation.realms)



    def test_insertData(self):
        self.init("insert")
        operation.insertData()

        auctions = db.get("Select * from auctionhouses", all=True)
        sold_auctions = db.get("Select * from soldauctions", all=True)
        items = db.get("Select * from items", all=True)
        classes = db.get("Select * from classes", all=True)
        subclasses = db.get("Select * from subclasses", all=True)
        pets = db.get("Select * from pets", all=True)
        mounts = db.get("Select * from mounts", all=True)

        #testing auctions
        self.assertEqual(2, len(auctions))
        self.assertEqual(1096, auctions[0][0])
        self.assertEqual(10569, auctions[0][1])
        self.assertEqual(25, auctions[0][2])
        self.assertEqual(0, auctions[0][3])
        self.assertEqual(1, auctions[0][4])
        self.assertEqual(52, auctions[0][5])
        self.assertEqual("SHORT", auctions[0][6])
        self.assertEqual(24.9, auctions[0][7])
        self.assertEqual(52, auctions[0][8])
        self.assertEqual(True, auctions[0][9] == auctions[0][10])

        self.assertEqual(1096, auctions[1][0])
        self.assertEqual(10570, auctions[1][1])
        self.assertEqual(35, auctions[1][2])
        self.assertEqual(0, auctions[1][3])
        self.assertEqual(1, auctions[1][4])
        self.assertEqual(68, auctions[1][5])
        self.assertEqual("MEDIUM", auctions[1][6])
        self.assertEqual(62.5, auctions[1][7])
        self.assertEqual(68, auctions[1][8])
        self.assertEqual(True, auctions[1][9] == auctions[1][10])

        #testing sold_auctions
        self.assertEqual(1, len(sold_auctions))
        self.assertEqual(1096, sold_auctions[0][0])
        self.assertEqual(10570, sold_auctions[0][1])
        self.assertEqual(35, sold_auctions[0][2])
        self.assertEqual(0, sold_auctions[0][3])
        self.assertEqual(1, sold_auctions[0][4])
        self.assertEqual(68, sold_auctions[0][5])
        self.assertEqual("MEDIUM", sold_auctions[0][6])
        self.assertEqual(62.5, sold_auctions[0][7])
        self.assertEqual(68, sold_auctions[0][8])
        self.assertEqual(False, sold_auctions[0][10])

        #testing items
        self.assertEqual(2, len(items))
        self.assertEqual(25, items[0][0]) #id
        self.assertEqual(0, items[0][1]) #pet_id
        self.assertEqual(0, items[0][2]) #mount_id
        self.assertEqual(1, items[0][3]) #level
        self.assertEqual("Worn Shortsword", items[0][4]) #name
        self.assertEqual("Common", items[0][5]) #quality
        self.assertEqual(2, items[0][6]) #class_id
        self.assertEqual(7, items[0][7]) #subclass_id
        self.assertEqual("WEAPONMAINHAND", items[0][8]) #type
        self.assertEqual("Main Hand", items[0][9]) #subtype
        self.assertEqual(0, items[0][10]) #mean_price

        self.assertEqual(35, items[1][0])
        self.assertEqual(0, items[1][1])
        self.assertEqual(0, items[1][2])
        self.assertEqual(1, items[1][3])
        self.assertEqual("Bent Staff", items[1][4])
        self.assertEqual("Common", items[1][5])
        self.assertEqual(2, items[1][6])
        self.assertEqual(10, items[1][7])
        self.assertEqual("TWOHWEAPON", items[1][8])
        self.assertEqual("Two-Hand", items[1][9])
        self.assertEqual(68, items[1][10])

        # testing classes
        self.assertEqual(1, len(classes))
        self.assertEqual(2, classes[0][0]) #id
        self.assertEqual("Weapon", classes[0][1]) #name

        # testing subclasses
        self.assertEqual(2, len(subclasses))
        self.assertEqual(2, subclasses[0][0]) #class_id
        self.assertEqual(7, subclasses[0][1]) #id
        self.assertEqual("Sword", subclasses[0][2]) #name

        self.assertEqual(2, subclasses[1][0])
        self.assertEqual(10, subclasses[1][1])
        self.assertEqual("Staff", subclasses[1][2])

        # testing pets
        self.assertEqual(2, len(pets))
        self.assertEqual(39, pets[0][0]) #id
        self.assertEqual("Mechanical Squirrel", pets[0][1]) #name
        self.assertEqual("Mechanical", pets[0][2]) #type
        self.assertEqual("Profession", pets[0][3]) #source
        self.assertEqual("Factionless", pets[0][4]) #faction

        self.assertEqual(40, pets[1][0])
        self.assertEqual("Bombay Cat", pets[1][1])
        self.assertEqual("Beast", pets[1][2])
        self.assertEqual("Vendor", pets[1][3])
        self.assertEqual("Factionless", pets[1][4])

        # testing mounts
        self.assertEqual(2, len(mounts))
        self.assertEqual(69, mounts[0][0]) #id
        self.assertEqual("Rivendare's Deathcharger", mounts[0][1]) #name
        self.assertEqual("Drop", mounts[0][2]) #source
        self.assertEqual("Factionless", mounts[0][3]) #faction

        self.assertEqual(85, mounts[1][0])
        self.assertEqual("Swift Mistsaber", mounts[1][1])
        self.assertEqual("Vendor", mounts[1][2])
        self.assertEqual("Alliance", mounts[1][3])


    def test_updateData(self):
        self.init("update")
        operation.updateData()

        # testing auctions
        auction = db.get("Select * from auctionhouses")
        self.assertEqual(1096, auction[0]) #realm_id
        self.assertEqual(10569, auction[1]) #auction_id
        self.assertEqual(25, auction[2]) #item_id
        self.assertEqual(0, auction[3]) #pet_id
        self.assertEqual(1, auction[4]) #quantity
        self.assertEqual(52, auction[5]) #unit_price
        self.assertEqual("SHORT", auction[6]) #time_left
        self.assertEqual(24.9, auction[7]) #bid
        self.assertEqual(52, auction[8]) #buyout
        self.assertEqual(False, auction[9] == auction[10]) #last_updated

        # testing items
        item = db.get("Select * from items where id=25")
        self.assertEqual(25, item[0]) #id
        self.assertEqual(0, item[1]) #pet_id
        self.assertEqual(0, item[2]) #mount_id
        self.assertEqual(1, item[3]) #level
        self.assertEqual("Worn Shortsword", item[4]) #name
        self.assertEqual("Common", item[5]) #quality
        self.assertEqual(2, item[6]) #class_id
        self.assertEqual(7, item[7]) #subclass_id
        self.assertEqual("WEAPONMAINHAND", item[8]) #type
        self.assertEqual("Main Hand", item[9]) #subtype
        self.assertEqual(1, item[10]) #mean_price


    def test_setLiveData(self):
        operation.setLiveData(request)

        # testing mounts
        self.assertEqual(2, len(operation.live_data["mounts"]))
        self.assertEqual(True, 69 in operation.live_data["mounts"])
        self.assertEqual(True, 85 in operation.live_data["mounts"])
        self.assertEqual("Rivendare's Deathcharger", operation.live_data["mounts"][69].name)
        self.assertEqual("Swift Mistsaber", operation.live_data["mounts"][85].name)

        # testing pets
        self.assertEqual(2, len(operation.live_data["pets"]))
        self.assertEqual(True, 39 in operation.live_data["pets"])
        self.assertEqual(True, 40 in operation.live_data["pets"])
        self.assertEqual("Mechanical Squirrel", operation.live_data["pets"][39].name)
        self.assertEqual("Bombay Cat", operation.live_data["pets"][40].name)

        # testing classes
        classes = operation.live_data["classes"]
        self.assertEqual(1, len(classes))
        self.assertEqual(True, 2 in classes)
        self.assertEqual("Weapon", classes[2].name)

        # testing items
        items = operation.live_data["items"]
        self.assertEqual(3, len(items))
        self.assertEqual(True, 82800 in items)
        self.assertEqual(True, 25 in items)
        self.assertEqual(True, 35 in items)
        self.assertEqual({}, items[82800])
        self.assertEqual("Worn Shortsword", items[25].name)
        self.assertEqual("Bent Staff", items[35].name)
        self.assertEqual(0, items[25].sold)
        self.assertEqual(0, items[25].price)
        self.assertEqual(0, items[25].mean_price)
        self.assertEqual(1, items[35].sold)
        self.assertEqual(68, items[35].price)
        self.assertEqual(68, items[35].mean_price)

        # testing auctions
        auctions = operation.live_data["auctions"][realm.id]
        self.assertEqual(1, len(auctions))
        self.assertEqual(True, 10569 in auctions)
        self.assertEqual("Worn Shortsword", auctions[10569].Item.name)




    def test_update(self):
        operation.update()
        self.assertEqual({}, operation.insert_data)
        self.assertEqual({}, operation.update_data)



    def test_setTimePosted(self):
        from operations import setTimePosted
        from datetime import datetime

        #testing test case
        test_time = setTimePosted(test=True)
        self.assertEqual(12, test_time.hour)
        self.assertEqual(30, test_time.minute)
        self.assertEqual(30, test_time.second)
        self.assertEqual(500000, test_time.microsecond)

        # testing not testcase
        now = datetime.now()
        time = setTimePosted()
        self.assertEqual(now.hour, time.hour)




    @unittest.skip
    def test_setTimeSold(self):
        pass



def reset():
    db.clearAll()



if __name__ == "__main__":
    logger = Logger(os.getcwd())
    db = Database(DATABASE, logger, test=True)
    reset()
    operation = Operation(db, logger)
    request = Request(CREDENTIALS, db, logger)
    realm = Realm(1096, db, logger, request)
    unittest.main()
