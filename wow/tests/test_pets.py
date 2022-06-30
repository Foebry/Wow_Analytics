import unittest
import os

print("test_pets")


class PetTest(unittest.TestCase):

    @staticmethod
    def init():
        from pets import Pet
        from operations import Operation
        from Requests import Request
        from databases.Database import Database
        from logger.Logger import Logger
        from config import DATABASE, CREDENTIALS

        logger = Logger(os.getcwd())
        db = Database(DATABASE, logger, test=True, testcase=True)
        operation = Operation(db, logger)
        request = Request(CREDENTIALS, db, logger)

        new_pet = Pet(operation, request, 39)
        rebuild_pet = Pet(_id=40, **{"name":"Bombay Cat", "type":"Beast", "faction":"Factionless", "source":"Vendor"})

        return new_pet, rebuild_pet, request, operation



    def test_init(self):

        # testing new pet
        pet = new_pet
        self.assertEqual(39, pet.id)
        self.assertEqual("Mechanical Squirrel", pet.name)
        self.assertEqual("Mechanical", pet.type)
        self.assertEqual("Factionless", pet.faction)
        self.assertEqual("Profession", pet.source)


        # testing rebuild pet
        pet = rebuild_pet
        self.assertEqual(40, pet.id)
        self.assertEqual("Bombay Cat", pet.name)
        self.assertEqual("Beast", pet.type)
        self.assertEqual("Factionless", pet.faction)
        self.assertEqual("Vendor", pet.source)



    def test_setData(self):
        data = new_pet.setData(operation, request, True)
        self.assertEqual(5, len(data.keys()))
        self.assertEqual(True, "_id" in data)
        self.assertEqual(True, "type" in data)
        self.assertEqual(True, "source" in data)
        self.assertEqual(True, "faction" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(39, data["_id"])
        self.assertEqual("Mechanical", data["type"])
        self.assertEqual("Profession", data["source"])
        self.assertEqual("Factionless", data["faction"])
        self.assertEqual("Mechanical Squirrel", data["name"])

        data = rebuild_pet.setData(operation, request, True)
        self.assertEqual(5, len(data.keys()))
        self.assertEqual(True, "_id" in data)
        self.assertEqual(True, "type" in data)
        self.assertEqual(True, "source" in data)
        self.assertEqual(True, "faction" in data)
        self.assertEqual(True, "name" in data)
        self.assertEqual(40, data["_id"])
        self.assertEqual("Beast", data["type"])
        self.assertEqual("Vendor", data["source"])
        self.assertEqual("Factionless", data["faction"])
        self.assertEqual("Bombay Cat", data["name"])


    def test_insert(self):
        operation.insert_data["pets"] = []
        insert_pets = operation.insert_data["pets"]
        new_pet.insert(operation)
        rebuild_pet.insert(operation)

        self.assertEqual(2, len(insert_pets))
        self.assertEqual(new_pet, insert_pets[0])
        self.assertEqual(rebuild_pet, insert_pets[1])




if __name__ == "__main__":
    new_pet, rebuild_pet, request, operation = PetTest.init()
    unittest.main()
