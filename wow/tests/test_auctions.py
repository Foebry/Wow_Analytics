import unittest
import os
import datetime

from auctions import SoldAuction, Auction
from logger.Logger import Logger
from databases.Database import Database
from Requests import Request
from operations import Operation
from realms import Realm
from config import CREDENTIALS, DATABASE

print("test_auctions")


def init():

    new_auction = Auction(realm, operation, request, False, *(1, 25, {"_id":0}, 1, 50, "LONG", 49, 50))
    realm.previous_auctions[new_auction.id] = new_auction
    existing_auction = Auction(realm, operation, request, True, *(1, 25, {"_id":0}, 1, 50, "SHORT", 49, 50))

    new_item = Auction(realm, operation, request, False, *(2, 35, {"_id":0}, 1, 80, "MEDIUM", 60, 80))
    existing_item = Auction(realm, operation, request, False, *(3, 25, {"_id":0}, 1, 60, "VERY_LONG", 55, 60))

    first_pet = Auction(realm, operation, request, False, *(4, 82800, {"_id":39, "quality":0, "level":1, "breed_id":0}, 1, 100, "LONG", 99, 100))
    new_pet = Auction(realm, operation, request, False, *(5, 82800, {"_id":40, "quality":1, "level":1, "breed_id":0}, 1, 200, "MEDIUM", 150, 200))
    existing_pet = Auction(realm, operation, request, False, *(6, 82800, {"_id":39, "quality":0, "level":5, "breed_id":0}, 1, 500, "SHORT", 475, 500))
    new_mount = Auction(realm, operation, request, False, *(7, 34060, {"_id":0}, 1, 5000, "VERY_LONG", 4999, 5000))
    new_mount.time_posted -= datetime.timedelta(hours=1)
    new_mount.last_updated = new_mount.time_posted

    kwargs = {"realm":realm, "_id":1, "item_id":25, "pet_id":0,
              "quantity":1, "unit_price":50, "time_left":"SHORT", "bid":49,
              "buyout":50, "time_posted":new_auction.time_posted,
              "last_updated":existing_auction.last_updated, "Item":existing_auction.Item}

    rebuild_auction = Auction(**kwargs)

    auction_1 = Auction(realm, operation, request, False, *(10, 210, {"_id":0}, 1, 155, "SHORT", 145, 155))
    auction_2 = Auction(realm, operation, request, False, *(11, 210, {"_id":0}, 1, 155, "MEDIUM", 145, 155))
    auction_3 = Auction(realm, operation, request, False, *(12, 210, {"_id":0}, 1, 160, "MEDIUM", 145, 160))
    auction_4 = Auction(realm, operation, request, False, *(13, 210, {"_id":0}, 1, 150, "LONG", 145, 150))
    auction_5 = Auction(realm, operation, request, False, *(14, 210, {"_id":0}, 1, 150, "MEDIUM", 145, 150))
    auction_6 = Auction(realm, operation, request, False, *(15, 210, {"_id":0}, 1, 150, "VERY_LONG", 145, 150))

    auctions_test_sold_auction = [auction_1, auction_2, auction_3, auction_4, auction_5, auction_6]
    for auction in auctions_test_sold_auction:
        auction.time_posted -= datetime.timedelta(hours=1)
        auction.last_updated = auction.time_posted

    return kwargs, new_auction, existing_auction, new_item, existing_item, first_pet, new_pet, existing_pet, rebuild_auction, auctions_test_sold_auction, new_mount


class AuctionTest(unittest.TestCase):

    def test_init(self):

        # testing new_auction
        auction = args[0]
        self.assertEqual(1, auction.id)
        self.assertEqual(realm, auction.realm)
        self.assertEqual(25, auction.item_id)
        self.assertEqual(0, auction.pet_id)
        self.assertEqual(1, auction.quantity)
        self.assertEqual(50, auction.unit_price)
        self.assertEqual("LONG", auction.time_left)
        self.assertEqual(49, auction.bid)
        self.assertEqual(50, auction.buyout)
        self.assertEqual("Worn Shortsword", auction.Item.name)
        self.assertEqual(True, auction.time_posted == auction.last_updated)

        # testing existing_auction
        auction = args[1]
        self.assertEqual(1, auction.id)
        self.assertEqual(realm, auction.realm)
        self.assertEqual(25, auction.item_id)
        self.assertEqual(0, auction.pet_id)
        self.assertEqual(1, auction.quantity)
        self.assertEqual(50, auction.unit_price)
        self.assertEqual("SHORT", auction.time_left)
        self.assertEqual(49, auction.bid)
        self.assertEqual(50, auction.buyout)
        self.assertEqual("Worn Shortsword", auction.Item.name)
        self.assertEqual(False, auction.time_posted == auction.last_updated)

        # testing new_item
        auction = args[2]
        self.assertEqual(2, auction.id)
        self.assertEqual(realm, auction.realm)
        self.assertEqual(35, auction.item_id)
        self.assertEqual(0, auction.pet_id)
        self.assertEqual(1, auction.quantity)
        self.assertEqual(80, auction.unit_price)
        self.assertEqual("MEDIUM", auction.time_left)
        self.assertEqual(60, auction.bid)
        self.assertEqual(80, auction.buyout)
        self.assertEqual("Bent Staff", auction.Item.name)
        self.assertEqual(True, auction.time_posted == auction.last_updated)

        # testing existing_item
        auction = args[3]
        self.assertEqual(3, auction.id)
        self.assertEqual(realm, auction.realm)
        self.assertEqual(25, auction.item_id)
        self.assertEqual(0, auction.pet_id)
        self.assertEqual(1, auction.quantity)
        self.assertEqual(60, auction.unit_price)
        self.assertEqual("VERY_LONG", auction.time_left)
        self.assertEqual(55, auction.bid)
        self.assertEqual(60, auction.buyout)
        self.assertEqual("Worn Shortsword", auction.Item.name)
        self.assertEqual(True, auction.time_posted == auction.last_updated)

        # testing first_pet
        auction = args[4]
        self.assertEqual(4, auction.id)
        self.assertEqual(realm, auction.realm)
        self.assertEqual(82800, auction.item_id)
        self.assertEqual(39, auction.pet_id)
        self.assertEqual(1, auction.quantity)
        self.assertEqual(100, auction.unit_price)
        self.assertEqual("LONG", auction.time_left)
        self.assertEqual(99, auction.bid)
        self.assertEqual(100, auction.buyout)
        self.assertEqual("Pet Cage", auction.Item.name)
        self.assertEqual("Mechanical Squirrel", auction.Item.Pet.name)
        self.assertEqual(True, auction.time_posted == auction.last_updated)

        # testing new_pet
        auction = args[5]
        self.assertEqual(5, auction.id)
        self.assertEqual(realm, auction.realm)
        self.assertEqual(82800, auction.item_id)
        self.assertEqual(40, auction.pet_id)
        self.assertEqual(1, auction.quantity)
        self.assertEqual(200, auction.unit_price)
        self.assertEqual("MEDIUM", auction.time_left)
        self.assertEqual(150, auction.bid)
        self.assertEqual(200, auction.buyout)
        self.assertEqual("Pet Cage", auction.Item.name)
        self.assertEqual("Bombay Cat", auction.Item.Pet.name)
        self.assertEqual(True, auction.time_posted == auction.last_updated)

        # testing existing_pet
        auction = args[6]
        self.assertEqual(6, auction.id)
        self.assertEqual(realm, auction.realm)
        self.assertEqual(82800, auction.item_id)
        self.assertEqual(39, auction.pet_id)
        self.assertEqual(1, auction.quantity)
        self.assertEqual(500, auction.unit_price)
        self.assertEqual("SHORT", auction.time_left)
        self.assertEqual(475, auction.bid)
        self.assertEqual(500, auction.buyout)
        self.assertEqual("Pet Cage", auction.Item.name)
        self.assertEqual("Mechanical Squirrel", auction.Item.Pet.name)
        self.assertEqual(True, auction.time_posted == auction.last_updated)

        # testing rebuilding auction
        auction = args[7]
        self.assertEqual(kwargs["_id"], auction.id)
        self.assertEqual(kwargs["realm"], auction.realm)
        self.assertEqual(kwargs["item_id"], auction.item_id)
        self.assertEqual(kwargs["pet_id"], auction.pet_id)
        self.assertEqual(kwargs["quantity"], auction.quantity)
        self.assertEqual(kwargs["unit_price"], auction.unit_price)
        self.assertEqual(kwargs["time_left"], auction.time_left)
        self.assertEqual(kwargs["bid"], auction.bid)
        self.assertEqual(kwargs["buyout"], auction.buyout)
        self.assertEqual(kwargs["time_posted"], auction.time_posted)
        self.assertEqual(kwargs["last_updated"], auction.last_updated)
        self.assertEqual("Worn Shortsword", auction.Item.name)

        self.assertEqual(13, len(operation.insert_data["auctions"][realm.id]))


    def test_insert(self):
        operation.insert_data["auctions"][realm.id] = []
        auction_new_auction = args[0]
        auction_new_item = args[2]
        auction_existing_item = args[3]
        auction_first_pet = args[4]
        auction_new_pet = args[5]
        auction_existing_pet = args[6]

        auction_new_auction.insert(operation)
        auction_new_item.insert(operation)
        auction_existing_item.insert(operation)
        auction_first_pet.insert(operation)
        auction_new_pet.insert(operation)
        auction_existing_pet.insert(operation)

        insert_auctions = operation.insert_data["auctions"][realm.id]

        self.assertEqual(6, len(insert_auctions))
        self.assertEqual(auction_new_auction, insert_auctions[0])
        self.assertEqual(auction_new_item, insert_auctions[1])
        self.assertEqual(auction_existing_item, insert_auctions[2])
        self.assertEqual(auction_first_pet, insert_auctions[3])
        self.assertEqual(auction_new_pet, insert_auctions[4])
        self.assertEqual(auction_existing_pet, insert_auctions[5])


    def test_update(self):
        operation.update_data["auctions"][realm.id] = []
        new_auction = args[0]
        existing_auction = args[1]

        existing_auction.update(operation, realm, new_auction)
        update_auctions = operation.update_data["auctions"][realm.id]

        self.assertEqual(1, len(update_auctions))
        self.assertEqual(existing_auction, update_auctions[0])



class SoldAuctionTest(unittest.TestCase):

    def test_init(self):
        auction = args[0]
        auction.time_posted -= datetime.timedelta(hours=1)
        auction.last_updated = auction.time_posted
        sold_auction = SoldAuction(operation, True, *(auction, 1, 25, 0, 1, 50, "SHORT", 49, 50, auction.time_posted, False))

        self.assertEqual(auction, sold_auction.Auction)
        self.assertEqual(realm, sold_auction.realm)
        self.assertEqual(1, sold_auction.id)
        self.assertEqual(25, sold_auction.item_id)
        self.assertEqual(0, sold_auction.pet_id)
        self.assertEqual(1, sold_auction.quantity)
        self.assertEqual("SHORT", sold_auction.time_left)
        self.assertEqual(49, sold_auction.bid)
        self.assertEqual(50, sold_auction.buyout)
        self.assertEqual(auction.time_posted, sold_auction.time_posted)
        self.assertEqual(True, sold_auction.time_sold > sold_auction.time_posted)
        self.assertEqual(False, sold_auction.partial)


    def test_insert(self):
        operation.insert_data["sold_auctions"] = {}
        operation.insert_data["sold_auctions"][realm.id] = []
        insert_auctions = operation.insert_data["sold_auctions"][realm.id]

        auction_2 = args[1]
        auction_3 = args[2]

        auction_2.time_posted -= datetime.timedelta(hours=1)
        auction_3.time_posted -= datetime.timedelta(hours=1)
        auction_2.last_updated = auction_2.time_posted
        auction_3.last_updated = auction_3.time_posted

        sold_auction_2 = SoldAuction(operation, True, *(auction_2, 2, 35, 0, 1, 80, "MEDIUM", 60, 80, auction_2.time_posted, False))
        sold_auction_3 = SoldAuction(operation, True, *(auction_3, 3, 25, 0, 1, 60, "LONG", 55, 60, auction_3.time_posted, False))

        sold_auction_2.insert(operation)
        sold_auction_3.insert(operation)

        self.assertEqual(2, len(insert_auctions))
        self.assertEqual(True, sold_auction_2 in insert_auctions)
        self.assertEqual(True, sold_auction_3 in insert_auctions)


    def test_isValidSoldAuction(self):

        # test True for only auction item_id
        soldauction = SoldAuction(operation, True, *(args[-1], 7, 34060, 0, 1, 5000, "VERY_LONG", 4999, 5000, args[-1].time_posted, False))
        insert_auctions = operation.insert_data["sold_auctions"][soldauction.realm.id]
        auctions_to_check = [
                            insert_auctions[x] for x in range(len(insert_auctions))
                            if insert_auctions[x].Auction.Item.id == soldauction.Auction.Item.id
                            ]
        self.assertEqual(True, soldauction.isValidSoldAuction(operation, auctions_to_check))

        insert_auctions = operation.insert_data["sold_auctions"][realm.id]
        auctions = args[-2]

        sold_auction_1 = SoldAuction(operation, True, *(auctions[0], 10, 210, 0, 1, 155, "SHORT", 145, 155, auctions[0].time_posted, False))
        sold_auction_2 = SoldAuction(operation, True, *(auctions[1], 11, 210, 0, 1, 155, "MEDIUM", 145, 155, auctions[1].time_posted, False))
        sold_auction_3 = SoldAuction(operation, True, *(auctions[2], 12, 210, 0, 1, 160, "MEDIUM", 145, 160, auctions[2].time_posted, False))
        sold_auction_4 = SoldAuction(operation, True, *(auctions[3], 13, 210, 0, 1, 150, "LONG", 145, 150, auctions[3].time_posted, False))
        sold_auction_5 = SoldAuction(operation, True, *(auctions[4], 14, 210, 0, 1, 155, "MEDIUM", 145, 155, auctions[4].time_posted, False))
        sold_auction_6 = SoldAuction(operation, True, *(auctions[5], 15, 210, 0, 1, 150, "VERY_LONG", 145, 150), auctions[5].time_posted, False)

        before = len(realm.auctions)

        self.assertEqual(False, sold_auction_1.isValidSoldAuction(operation, [])) # False for SHORT duration
        self.assertEqual(True, sold_auction_2.isValidSoldAuction(operation, [])) # Cheapest and first in row
        self.assertEqual(False, sold_auction_3.isValidSoldAuction(operation, [sold_auction_2])) # False for not cheapest
        self.assertEqual(True, sold_auction_4.isValidSoldAuction(operation, [sold_auction_2])) # Cheapest and not undercut
        self.assertEqual(False, sold_auction_5.isValidSoldAuction(operation, [sold_auction_2, sold_auction_4])) # False for undercut
        self.assertEqual(True, sold_auction_6.isValidSoldAuction(operation, auctions_to_check)) # Cheapest and not undercut

        after = len(realm.auctions)
        self.assertEqual(True, before > after)


if __name__ == "__main__":
    logger = Logger(os.getcwd())
    db = Database(DATABASE, logger, True, True)
    request = Request(CREDENTIALS, db, logger)
    operation = Operation(db, logger)
    realm = Realm(1096, db, logger, request)
    kwargs, *args = init()
    unittest.main()
