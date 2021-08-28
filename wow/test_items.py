import unittest
import os

from Requests import Request
from operations import Operation
from logger.Logger import Logger
from databases.Database import Database
from config import DATABASE, CREDENTIALS
from realms import Realm


class ItemTest(unittest.TestCase):


    @staticmethod
    def init():

        from items import Item
        from classes import Class, Subclass
        from pets import Pet
        from mounts import Mount

        weapon_class = Class(operation, request, 2)
        battle_pet_class = Class(operation, request, 17)
        misc_class = Class(operation, request, 15)
        staff_subclass = Subclass(operation, request, 2, 10)
        pet_subclass = Subclass(operation, request, 17, 0)
        mount_subclass = Subclass(operation, request, 15, 5)

        existing_pet = Pet(operation, request, 40)
        existing_mount = Mount(operation, request, 240)

        new_item_item = Item(operation, request, 25)
        new_item_pet = Item(operation, request, 82800, pet_data={"_id":39, "quality":3, "level":1, "breed_id":5})
        new_item_mount = Item(operation, request, 34060)
        new_items = (new_item_item, new_item_pet, new_item_mount)

        rebuild_item_item = Item(**{"_id":35, "pet":{"_id":0}, "mount":{"_id":0}, "level":1, "name":"Bent Staff", "quality":"Common", "item_class":2, "item_subclass":10, "type":"TWOHWEAPON", "subtype":"Two-Hand", "sold":0, "price":0, "mean_price":0, "Pet":None, "Mount":None, "Class":weapon_class, "Subclass":staff_subclass})
        rebuild_item_pet = Item(**{"_id":82800, "pet":{"_id":40}, "mount":{"_id":0},"level":25, "name":"Pet Cage", "quality":"Rare", "item_class":17, "item_subclass":0, "type":"NON_EQUIP", "subtype":"Non-equippable", "sold":0, "price":0, "mean_price":0, "Pet":existing_pet, "Mount":None, "Class":battle_pet_class, "Subclass":pet_subclass})
        rebuild_item_mount = Item(**{"_id":41058, "pet":{"_id":0}, "mount":{"_id":240},"level":30, "name":"Mechano-Hog","quality":"Epic", "item_class":15, "item_subclass":5, "type":"NON_EQUIP", "subtype":"Non-equippable", "sold":0, "price":0, "mean_price":0, "Pet":None, "Mount":existing_mount, "Class":misc_class, "Subclass":mount_subclass})
        rebuild_items = (rebuild_item_item, rebuild_item_pet, rebuild_item_mount)

        return new_items, rebuild_items



    def test_init(self):

        # test new item_item
        item = new_items[0]
        self.assertEqual(25, item.id)
        self.assertEqual(0, item.mount_id)
        self.assertEqual(0, item.pet_id)
        self.assertEqual("Worn Shortsword", item.name)
        self.assertEqual(1, item.level)
        self.assertEqual("Common", item.quality)
        self.assertEqual(2, item.class_id)
        self.assertEqual(7, item.subclass_id)
        self.assertEqual("WEAPONMAINHAND", item.type)
        self.assertEqual("Main Hand", item.subtype)
        self.assertEqual(0, item.sold)
        self.assertEqual(0, item.price)
        self.assertEqual(0, item.mean_price)
        self.assertEqual(None, item.Pet)
        self.assertEqual(None, item.Mount)

        # test new_item_pet
        item = new_items[1]
        self.assertEqual(82800, item.id)
        self.assertEqual(0, item.mount_id)
        self.assertEqual(39, item.pet_id)
        self.assertEqual("Pet Cage", item.name)
        self.assertEqual(1, item.level)
        self.assertEqual("Rare", item.quality)
        self.assertEqual(17, item.class_id)
        self.assertEqual(0, item.subclass_id)
        self.assertEqual("NON_EQUIP", item.type)
        self.assertEqual("Non-equippable", item.subtype)
        self.assertEqual(0, item.sold)
        self.assertEqual(0, item.price)
        self.assertEqual(0, item.mean_price)
        self.assertEqual(39, item.Pet.id)
        self.assertEqual("Mechanical Squirrel", item.Pet.name)
        self.assertEqual(None, item.Mount)

        # test new_item_mount
        item = new_items[2]
        self.assertEqual(34060, item.id)
        self.assertEqual(205, item.mount_id)
        self.assertEqual("Flying Machine", item.name)
        self.assertEqual(30, item.level)
        self.assertEqual("Rare", item.quality)
        self.assertEqual(15, item.class_id)
        self.assertEqual(5, item.subclass_id)
        self.assertEqual("NON_EQUIP", item.type)
        self.assertEqual("Non-equippable", item.subtype)
        self.assertEqual(0, item.sold)
        self.assertEqual(0, item.price)
        self.assertEqual(0, item.mean_price)
        self.assertEqual(None, item.Pet)
        self.assertEqual(205, item.Mount.id)
        self.assertEqual("Flying Machine", item.Mount.name)


        # test rebuild item_item
        item = rebuild_items[0]
        self.assertEqual(35, item.id)
        self.assertEqual(0, item.mount_id)
        self.assertEqual(0, item.pet_id)
        self.assertEqual("Bent Staff", item.name)
        self.assertEqual(1, item.level)
        self.assertEqual("Common", item.quality)
        self.assertEqual(2, item.class_id)
        self.assertEqual(10, item.subclass_id)
        self.assertEqual("TWOHWEAPON", item.type)
        self.assertEqual("Two-Hand", item.subtype)
        self.assertEqual(0, item.sold)
        self.assertEqual(0, item.price)
        self.assertEqual(0, item.mean_price)
        self.assertEqual(None, item.Pet)
        self.assertEqual(None, item.Mount)

        # test rebuild item_pet
        item = rebuild_items[1]
        self.assertEqual(82800, item.id)
        self.assertEqual(0, item.mount_id)
        self.assertEqual(40, item.pet_id)
        self.assertEqual("Pet Cage", item.name)
        self.assertEqual(25, item.level)
        self.assertEqual("Rare", item.quality)
        self.assertEqual(17, item.class_id)
        self.assertEqual(0, item.subclass_id)
        self.assertEqual("NON_EQUIP", item.type)
        self.assertEqual("Non-equippable", item.subtype)
        self.assertEqual(0, item.sold)
        self.assertEqual(0, item.price)
        self.assertEqual(0, item.mean_price)
        self.assertEqual(40, item.Pet.id)
        self.assertEqual("Bombay Cat", item.Pet.name)
        self.assertEqual(None, item.Mount)

        # test rebuild item_mount
        item = rebuild_items[2]
        self.assertEqual(41058, item.id)
        self.assertEqual(240, item.mount_id)
        self.assertEqual(0, item.pet_id)
        self.assertEqual("Mechano-Hog", item.name)
        self.assertEqual(30, item.level)
        self.assertEqual("Epic", item.quality)
        self.assertEqual(15, item.class_id)
        self.assertEqual(5, item.subclass_id)
        self.assertEqual("NON_EQUIP", item.type)
        self.assertEqual("Non-equippable", item.subtype)
        self.assertEqual(0, item.sold)
        self.assertEqual(0, item.price)
        self.assertEqual(0, item.mean_price)
        self.assertEqual(None, item.Pet)
        self.assertEqual(240, item.Mount.id)
        self.assertEqual("Mechano-Hog", item.Mount.name)


    def test_setData(self):
        new_item_item = new_items[0]
        data = new_item_item.setData(operation, request, {"_id":0}, True)
        self.assertEqual(13, len(data.keys()))
        self.assertEqual(True, "pet" in data)
        self.assertEqual(True, "mount" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(True, "level" in data)
        self.assertEqual(True, "quality" in data)
        self.assertEqual(True, "item_class" in data)
        self.assertEqual(True, "item_subclass" in data)
        self.assertEqual(True, "type" in data)
        self.assertEqual(True, "subtype" in data)
        self.assertEqual(True, "sold" in data)
        self.assertEqual(True, "price" in data)
        self.assertEqual(True, "mean_price" in data)
        self.assertEqual(True, "_id" in data)
        self.assertEqual({"_id":0}, data["pet"])
        self.assertEqual({"_id":0}, data["mount"])
        self.assertEqual("Worn Shortsword", data["name"])
        self.assertEqual(1, data["level"])
        self.assertEqual("Common", data["quality"])
        self.assertEqual(2, data["item_class"])
        self.assertEqual(7, data["item_subclass"])
        self.assertEqual("WEAPONMAINHAND", data["type"])
        self.assertEqual("Main Hand", data["subtype"])
        self.assertEqual(0, data["sold"])
        self.assertEqual(0, data["price"])
        self.assertEqual(0, data["mean_price"])
        self.assertEqual(25, data["_id"])

        new_item_pet = new_items[1]
        data = new_item_pet.setData(operation, request, {"_id":39, "quality":3, "level":1, "breed_id":5}, True)
        self.assertEqual(13, len(data.keys()))
        self.assertEqual(True, "pet" in data)
        self.assertEqual(True, "mount" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(True, "level" in data)
        self.assertEqual(True, "quality" in data)
        self.assertEqual(True, "item_class" in data)
        self.assertEqual(True, "item_subclass" in data)
        self.assertEqual(True, "type" in data)
        self.assertEqual(True, "subtype" in data)
        self.assertEqual(True, "sold" in data)
        self.assertEqual(True, "price" in data)
        self.assertEqual(True, "mean_price" in data)
        self.assertEqual(True, "_id" in data)
        self.assertEqual({"_id":39}, data["pet"])
        self.assertEqual({"_id":0}, data["mount"])
        self.assertEqual("Pet Cage", data["name"])
        self.assertEqual(1, data["level"])
        self.assertEqual("Rare", data["quality"])
        self.assertEqual(17, data["item_class"])
        self.assertEqual(0, data["item_subclass"])
        self.assertEqual("NON_EQUIP", data["type"])
        self.assertEqual("Non-equippable", data["subtype"])
        self.assertEqual(0, data["sold"])
        self.assertEqual(0, data["price"])
        self.assertEqual(0, data["mean_price"])
        self.assertEqual(82800, data["_id"])

        new_item_mount = new_items[2]
        data = new_item_mount.setData(operation, request, {"_id":0}, True)
        self.assertEqual(13, len(data.keys()))
        self.assertEqual(True, "pet" in data)
        self.assertEqual(True, "mount" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(True, "level" in data)
        self.assertEqual(True, "quality" in data)
        self.assertEqual(True, "item_class" in data)
        self.assertEqual(True, "item_subclass" in data)
        self.assertEqual(True, "type" in data)
        self.assertEqual(True, "subtype" in data)
        self.assertEqual(True, "sold" in data)
        self.assertEqual(True, "price" in data)
        self.assertEqual(True, "mean_price" in data)
        self.assertEqual(True, "_id" in data)
        self.assertEqual({"_id":0}, data["pet"])
        self.assertEqual({"_id":205}, data["mount"])
        self.assertEqual("Flying Machine", data["name"])
        self.assertEqual(30, data["level"])
        self.assertEqual("Rare", data["quality"])
        self.assertEqual(15, data["item_class"])
        self.assertEqual(5, data["item_subclass"])
        self.assertEqual("NON_EQUIP", data["type"])
        self.assertEqual("Non-equippable", data["subtype"])
        self.assertEqual(0, data["sold"])
        self.assertEqual(0, data["price"])
        self.assertEqual(0, data["mean_price"])
        self.assertEqual(34060, data["_id"])


    def test_insert(self):
        operation.insert_data["items"] = []
        for item in new_items: item.insert(operation)
        insert_items = operation.insert_data["items"]

        self.assertEqual(3, len(insert_items))
        self.assertEqual(new_items[0], insert_items[0])
        self.assertEqual(new_items[1], insert_items[1])
        self.assertEqual(new_items[2], insert_items[2])


    def test_update(self):
        operation.update_data["items"] = []
        for item in new_items: item.update(operation)
        update_items = operation.update_data["items"]

        self.assertEqual(3, len(update_items))
        self.assertEqual(new_items[0], update_items[0])
        self.assertEqual(new_items[1], update_items[1])
        self.assertEqual(new_items[2], update_items[2])


    def test_updateMean(self):
        from auctions import SoldAuction, Auction
        from datetime import timedelta

        operation.live_data["auctions"][realm.id] = {}
        buyout = 50

        auction_item = Auction(realm, operation, request, False, *(realm, 1, 25, {"_id":0}, 1, buyout, "LONG", 45, buyout))
        auction_pet = Auction(realm, operation, request, False, *(realm, 2, 82800, {"_id":39, "quality":3, "level":1, "breed_id":5}, 2, buyout, "MEDIUM", 45, buyout*2))
        auction_mount = Auction(realm, operation, request, False, *(realm, 3, 34060, {"_id":0}, 3, buyout, "SHORT", 45, buyout*3))

        auction_item.time_posted -= timedelta(hours=1)
        auction_pet.time_posted -= timedelta(hours=1)
        auction_mount.time_posted -= timedelta(hours=1)
        auction_item.last_updated = auction_item.time_posted
        auction_pet.last_updated = auction_pet.time_posted
        auction_mount.last_updated = auction_mount.time_posted

        sold_auction_item = SoldAuction(operation, *(auction_item, 1, 25, 0, 1, buyout, "LONG", 45, buyout, auction_item.time_posted, False))
        sold_auction_pet = SoldAuction(operation, *(auction_pet, 2, 82800, 39, 2, buyout*2, "MEDIUM", 45, buyout*2, auction_pet.time_posted, False))
        sold_auction_mount = SoldAuction(operation, *(auction_mount, 3, 34060, 0, 3, buyout*3, "SHORT", 45, buyout*3, auction_mount.time_posted, False))

        item_item = new_items[0]
        item_pet = new_items[1]
        item_mount = new_items[2]

        item_item.updateMean(sold_auction_item, operation)
        item_pet.updateMean(sold_auction_pet, operation)
        item_mount.updateMean(sold_auction_mount, operation)

        self.assertEqual(50, item_item.mean_price)
        self.assertEqual(50, item_pet.mean_price)
        self.assertEqual(50, item_mount.mean_price)



if __name__ == "__main__":
    logger = Logger(os.getcwd())
    db = Database(DATABASE, logger, test=True)
    operation = Operation(db, logger)
    operation.live_data = {"auctions":{}, "items":{}, "classes":{}, "subclasses":{}, "pets":{}, "mounts":{}}
    request = Request(CREDENTIALS, db, logger)
    realm = Realm(1096, db, logger, request)
    new_items, rebuild_items = ItemTest.init()
    unittest.main()
